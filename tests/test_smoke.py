"""One smoke test per job, on the sample data."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pyarrow as pa
import pytest

from cancer_genome_atlas_engine import io
from cancer_genome_atlas_engine.config import Settings
from cancer_genome_atlas_engine.jobs import REGISTRY
from cancer_genome_atlas_engine.jobs.cluster_expression import Params as ClusterParams
from cancer_genome_atlas_engine.schemas import (
    CASES,
    CASES_DEMOGRAPHICS,
    CASES_DIAGNOSES,
    CASES_EXPOSURES,
    CLUSTER_SUMMARY,
    DEMOGRAPHIC_SUMMARY,
    EXPLAINED_VARIANCE,
    EXPOSURE_SUMMARY,
    EXPRESSION_CLUSTERS,
    EXPRESSION_COORDINATES,
    EXPRESSION_FILES_INFO,
    EXPRESSION_PROFILES,
    GENE_VARIANCE,
    TISSUE_SUMMARY,
)

REPO = Path(__file__).resolve().parent.parent
SETTINGS = Settings(sample_dir=REPO / "data" / "sample", output_dir=REPO / "output")

SAMPLE_TABLES = (
    "expression_files_info_raw",
    "cases_raw",
    "expression_profiles_raw",
    "expression_files_info",
    "cases",
    "expression_profiles",
    "cases_demographics",
    "cases_diagnoses",
    "cases_exposures",
    "gene_variance",
    "expression_coordinates",
    "explained_variance",
    "expression_clusters",
    "cluster_summary",
    "tissue_summary",
    "demographic_summary",
    "exposure_summary",
)


# The tolerance for values that depend only on exact linear algebra (PCA); it is far above
# the rounding differences between maths libraries and far below any real change.
PCA_TOLERANCE = 1e-6
SUM_TOLERANCE = 1e-9


@pytest.fixture(scope="module")
def tables() -> dict[str, object]:
    return {name: io.read_table(name, SETTINGS) for name in SAMPLE_TABLES}


def _groups(labels: dict[str, int]) -> set[frozenset[str]]:
    """The samples grouped by cluster number, without the numbers."""
    grouped: dict[int, set[str]] = {}
    for file_id, label in labels.items():
        grouped.setdefault(label, set()).add(file_id)
    return {frozenset(members) for members in grouped.values()}


def _partition(clusters: pa.Table) -> set[frozenset[str]]:
    return _groups(
        dict(
            zip(
                clusters.column("file_id").to_pylist(),
                clusters.column("kmeans_cluster").to_pylist(),
                strict=True,
            )
        )
    )


def run_job(name: str, inputs: dict, params=None):
    spec = REGISTRY[name]
    return spec.run(inputs=inputs, params=params if params is not None else spec.params_cls())


def test_clean_expression_files(tables: dict) -> None:
    outputs = run_job(
        "clean_expression_files", {"expression_files_info_raw": tables["expression_files_info_raw"]}
    )
    assert outputs["expression_files_info"].schema.equals(EXPRESSION_FILES_INFO)
    assert outputs["expression_files_info"].equals(
        tables["expression_files_info"].select(EXPRESSION_FILES_INFO.names)
    )
    assert outputs["expression_files_info"].num_rows == 9


def test_clean_cases(tables: dict) -> None:
    outputs = run_job("clean_cases", {"cases_raw": tables["cases_raw"]})
    assert outputs["cases"].schema.equals(CASES)
    assert outputs["cases"].equals(tables["cases"].select(CASES.names))


def test_clean_expression_profiles(tables: dict) -> None:
    outputs = run_job(
        "clean_expression_profiles", {"expression_profiles_raw": tables["expression_profiles_raw"]}
    )
    profiles = outputs["expression_profiles"]
    assert profiles.schema.equals(EXPRESSION_PROFILES)
    assert profiles.equals(tables["expression_profiles"].select(EXPRESSION_PROFILES.names))
    assert profiles.num_rows == 2700
    validated = profiles.column("fpkm_unstranded_validated").to_pylist()
    assert all(value is None or value >= 0 for value in validated)


def test_cases_demographics(tables: dict) -> None:
    outputs = run_job(
        "cases_demographics",
        {"cases": tables["cases"], "expression_files_info": tables["expression_files_info"]},
    )
    assert outputs["cases_demographics"].schema.equals(CASES_DEMOGRAPHICS)
    assert outputs["cases_demographics"].equals(
        tables["cases_demographics"].select(CASES_DEMOGRAPHICS.names)
    )


def test_cases_diagnoses(tables: dict) -> None:
    outputs = run_job(
        "cases_diagnoses",
        {"cases": tables["cases"], "expression_files_info": tables["expression_files_info"]},
    )
    assert outputs["cases_diagnoses"].schema.equals(CASES_DIAGNOSES)
    assert outputs["cases_diagnoses"].equals(
        tables["cases_diagnoses"].select(CASES_DIAGNOSES.names)
    )


def test_cases_exposures(tables: dict) -> None:
    outputs = run_job(
        "cases_exposures",
        {"cases": tables["cases"], "expression_files_info": tables["expression_files_info"]},
    )
    assert outputs["cases_exposures"].schema.equals(CASES_EXPOSURES)
    assert outputs["cases_exposures"].equals(
        tables["cases_exposures"].select(CASES_EXPOSURES.names)
    )


def test_select_variable_genes(tables: dict) -> None:
    outputs = run_job(
        "select_variable_genes", {"expression_profiles": tables["expression_profiles"]}
    )
    genes = outputs["gene_variance"]
    assert genes.schema.equals(GENE_VARIANCE)
    stored = tables["gene_variance"].select(GENE_VARIANCE.names)
    for name in ("gene_id", "gene_name", "samples"):
        assert genes.column(name).equals(stored.column(name))
    # Sums of floating-point values can differ in the last digits between platforms.
    for name in ("variance", "mean_expression"):
        np.testing.assert_allclose(
            genes.column(name).to_numpy(),
            stored.column(name).to_numpy(),
            rtol=SUM_TOLERANCE,
            atol=SUM_TOLERANCE,
        )
    assert genes.num_rows == 300
    variances = genes.column("variance").to_pylist()
    assert variances == sorted(variances, reverse=True)


def test_expression_dimensions(tables: dict) -> None:
    inputs = {
        "expression_profiles": tables["expression_profiles"],
        "gene_variance": tables["gene_variance"],
    }
    outputs = run_job("expression_dimensions", inputs)
    coordinates = outputs["expression_coordinates"]
    assert coordinates.schema.equals(EXPRESSION_COORDINATES)
    assert coordinates.num_rows == 9
    stored = tables["expression_coordinates"].select(EXPRESSION_COORDINATES.names)
    assert coordinates.column("file_id").equals(stored.column("file_id"))

    # PCA is deterministic: the stored components match to rounding error. The sign of a
    # component is fixed by scikit-learn's convention, so it is compared too.
    for name in ("pc1", "pc2", "pc3"):
        np.testing.assert_allclose(
            coordinates.column(name).to_numpy(),
            stored.column(name).to_numpy(),
            rtol=PCA_TOLERANCE,
            atol=PCA_TOLERANCE,
        )

    # t-SNE depends on the platform's maths libraries, so the stored embedding is not compared
    # value by value: it must have the right shape and be finite, and one seed must give one result.
    embedding = np.column_stack(
        [coordinates.column("tsne_1").to_numpy(), coordinates.column("tsne_2").to_numpy()]
    )
    assert embedding.shape == (9, 2)
    assert np.isfinite(embedding).all()
    assert np.ptp(embedding, axis=0).min() > 0
    again = run_job("expression_dimensions", inputs)
    assert again["expression_coordinates"].equals(coordinates)

    variance = outputs["explained_variance"]
    assert variance.schema.equals(EXPLAINED_VARIANCE)
    stored_variance = tables["explained_variance"].select(EXPLAINED_VARIANCE.names)
    assert variance.column("component").equals(stored_variance.column("component"))
    for name in ("explained_variance_ratio", "cumulative_variance"):
        np.testing.assert_allclose(
            variance.column(name).to_numpy(),
            stored_variance.column(name).to_numpy(),
            rtol=PCA_TOLERANCE,
            atol=PCA_TOLERANCE,
        )
    cumulative = variance.column("cumulative_variance").to_pylist()
    assert cumulative == sorted(cumulative)
    assert cumulative[-1] > 0.99


def test_cluster_expression(tables: dict) -> None:
    outputs = run_job(
        "cluster_expression",
        {
            "expression_coordinates": tables["expression_coordinates"],
            "cases_diagnoses": tables["cases_diagnoses"],
        },
    )
    clusters = outputs["expression_clusters"]
    assert clusters.schema.equals(EXPRESSION_CLUSTERS)
    assert clusters.num_rows == 9

    # Cluster numbers are arbitrary labels: compare the grouping, not the numbers.
    stored = tables["expression_clusters"].select(EXPRESSION_CLUSTERS.names)
    assert clusters.column("file_id").equals(stored.column("file_id"))
    assert _partition(clusters) == _partition(stored)
    assert set(clusters.column("kmeans_cluster").to_pylist()) <= set(range(4))

    # The summary counts the samples of each cluster and tissue in the clusters just made.
    summary = outputs["cluster_summary"]
    assert summary.schema.equals(CLUSTER_SUMMARY)
    expected: dict[tuple[int, str], int] = {}
    for row in clusters.to_pylist():
        key = (row["kmeans_cluster"], row["tissue_or_organ_of_origin"] or "")
        expected[key] = expected.get(key, 0) + 1
    assert {
        (row["kmeans_cluster"], row["tissue_or_organ_of_origin"]): row["samples"]
        for row in summary.to_pylist()
    } == expected


def test_cluster_expression_finds_separated_groups(tables: dict) -> None:
    """Three well-separated groups of three samples come out as exactly those groups."""
    files = tables["cases_diagnoses"].column("file_id").to_pylist()
    centres = [(-200.0, -200.0), (0.0, 200.0), (200.0, -200.0)]
    rows = [
        {
            "file_id": file_id,
            "pc1": 0.0,
            "pc2": 0.0,
            "pc3": 0.0,
            "tsne_1": centres[position // 3][0] + position % 3,
            "tsne_2": centres[position // 3][1] - position % 3,
        }
        for position, file_id in enumerate(files)
    ]
    coordinates = pa.Table.from_pylist(rows, schema=EXPRESSION_COORDINATES)
    outputs = run_job(
        "cluster_expression",
        {"expression_coordinates": coordinates, "cases_diagnoses": tables["cases_diagnoses"]},
        ClusterParams(n_clusters=3),
    )
    labels = dict(
        zip(
            outputs["expression_clusters"].column("file_id").to_pylist(),
            outputs["expression_clusters"].column("kmeans_cluster").to_pylist(),
            strict=True,
        )
    )
    groups = {frozenset(files[start : start + 3]) for start in (0, 3, 6)}
    assert _groups(labels) == groups


def test_cluster_expression_rejects_too_many_clusters(tables: dict) -> None:
    with pytest.raises(ValueError, match="n_clusters"):
        run_job(
            "cluster_expression",
            {
                "expression_coordinates": tables["expression_coordinates"],
                "cases_diagnoses": tables["cases_diagnoses"],
            },
            ClusterParams(n_clusters=50),
        )


def test_tissue_summary(tables: dict) -> None:
    outputs = run_job("tissue_summary", {"cases_diagnoses": tables["cases_diagnoses"]})
    assert outputs["tissue_summary"].schema.equals(TISSUE_SUMMARY)
    assert outputs["tissue_summary"].equals(tables["tissue_summary"].select(TISSUE_SUMMARY.names))
    rows = {
        row["tissue_or_organ_of_origin"]: row["samples"]
        for row in outputs["tissue_summary"].to_pylist()
    }
    assert rows["Breast, NOS"] == 3
    assert rows["Upper lobe, lung"] == 3


def test_demographic_summary(tables: dict) -> None:
    outputs = run_job("demographic_summary", {"cases_demographics": tables["cases_demographics"]})
    assert outputs["demographic_summary"].schema.equals(DEMOGRAPHIC_SUMMARY)
    assert outputs["demographic_summary"].equals(
        tables["demographic_summary"].select(DEMOGRAPHIC_SUMMARY.names)
    )
    assert sum(row["samples"] for row in outputs["demographic_summary"].to_pylist()) == 9


def test_exposure_summary(tables: dict) -> None:
    outputs = run_job("exposure_summary", {"cases_exposures": tables["cases_exposures"]})
    assert outputs["exposure_summary"].schema.equals(EXPOSURE_SUMMARY)
    assert outputs["exposure_summary"].equals(
        tables["exposure_summary"].select(EXPOSURE_SUMMARY.names)
    )
    assert sum(row["samples"] for row in outputs["exposure_summary"].to_pylist()) == 9
