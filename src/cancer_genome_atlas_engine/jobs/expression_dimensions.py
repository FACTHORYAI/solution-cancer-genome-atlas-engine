"""Reduce the expression matrix with PCA and t-SNE into per-sample coordinates."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pyarrow as pa
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler

from cancer_genome_atlas_engine.jobs._duck import align
from cancer_genome_atlas_engine.schemas import EXPLAINED_VARIANCE, EXPRESSION_COORDINATES

INPUTS = ("expression_profiles", "gene_variance")
OUTPUTS = ("expression_coordinates", "explained_variance")

MINIMUM_SAMPLES = 3
TSNE_INPUT_COMPONENTS = 20


@dataclass(frozen=True)
class Params:
    """Parameters for the dimensionality reduction."""

    n_pca_components: int = 50
    tsne_perplexity: float = 30.0
    tsne_max_iter: int = 1000
    random_state: int = 42


def run(inputs: dict[str, pa.Table], params: Params) -> dict[str, pa.Table]:
    """Return the per-sample coordinates and the variance each principal component explains."""
    matrix, file_ids = _expression_matrix(inputs["expression_profiles"], inputs["gene_variance"])
    n_samples, n_genes = matrix.shape
    if n_samples < MINIMUM_SAMPLES:
        message = (
            f"expression_dimensions needs at least {MINIMUM_SAMPLES} samples; "
            f"expression_profiles has {n_samples}"
        )
        raise ValueError(message)
    if n_genes < 2:
        message = f"expression_dimensions needs at least 2 genes; gene_variance has {n_genes}"
        raise ValueError(message)
    if params.n_pca_components < 1:
        message = f"Parameter n_pca_components is {params.n_pca_components}; it must be at least 1"
        raise ValueError(message)

    n_components = min(params.n_pca_components, n_samples, n_genes)
    scaled = StandardScaler().fit_transform(matrix)
    pca = PCA(n_components=n_components, random_state=params.random_state)
    reduced = pca.fit_transform(scaled)

    tsne_input = reduced[:, : min(TSNE_INPUT_COMPONENTS, n_components)]
    perplexity = max(2.0, min(params.tsne_perplexity, float(n_samples - 1)))
    embedding = TSNE(
        n_components=2,
        random_state=params.random_state,
        perplexity=perplexity,
        max_iter=params.tsne_max_iter,
        learning_rate=200.0,
        init="random",
    ).fit_transform(tsne_input)

    coordinates = _coordinates(file_ids, reduced, embedding)
    return {
        "expression_coordinates": align(coordinates, EXPRESSION_COORDINATES),
        "explained_variance": align(_explained_variance(pca), EXPLAINED_VARIANCE),
    }


def _expression_matrix(profiles: pa.Table, gene_variance: pa.Table) -> tuple[np.ndarray, list[str]]:
    """Build a samples-by-genes matrix of validated FPKM values, missing values as zero."""
    genes = [row["gene_id"] for row in gene_variance.to_pylist()]
    gene_position = {gene_id: position for position, gene_id in enumerate(genes)}
    file_ids = sorted(set(profiles.column("file_id").to_pylist()))
    file_position = {file_id: position for position, file_id in enumerate(file_ids)}
    matrix = np.zeros((len(file_ids), len(genes)), dtype=float)
    for row in profiles.to_pylist():
        gene_index = gene_position.get(row["gene_id"])
        file_index = file_position.get(row["file_id"])
        if gene_index is None or file_index is None:
            continue
        value = row["fpkm_unstranded_validated"]
        matrix[file_index, gene_index] = float(value) if value is not None else 0.0
    return matrix, file_ids


def _coordinates(file_ids: list[str], reduced: np.ndarray, embedding: np.ndarray) -> pa.Table:
    """Build the coordinate table, padding principal components beyond the third with zero."""
    rows = []
    for position, file_id in enumerate(file_ids):
        rows.append(
            {
                "file_id": file_id,
                "pc1": float(reduced[position, 0]),
                "pc2": float(reduced[position, 1]) if reduced.shape[1] > 1 else 0.0,
                "pc3": float(reduced[position, 2]) if reduced.shape[1] > 2 else 0.0,
                "tsne_1": float(embedding[position, 0]),
                "tsne_2": float(embedding[position, 1]),
            }
        )
    return pa.Table.from_pylist(rows, schema=EXPRESSION_COORDINATES)


def _explained_variance(pca: PCA) -> pa.Table:
    """Build the per-component explained-variance table."""
    ratios = pca.explained_variance_ratio_
    cumulative = np.cumsum(ratios)
    rows = [
        {
            "component": position + 1,
            "explained_variance_ratio": float(ratio),
            "cumulative_variance": float(total),
        }
        for position, (ratio, total) in enumerate(zip(ratios, cumulative, strict=True))
    ]
    return pa.Table.from_pylist(rows, schema=EXPLAINED_VARIANCE)
