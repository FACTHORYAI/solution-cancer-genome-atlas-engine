"""Cluster the reduced samples with K-means and summarise the clusters by tissue."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pyarrow as pa
from sklearn.cluster import KMeans

from cancer_genome_atlas_engine import io
from cancer_genome_atlas_engine.jobs._duck import align, run_query
from cancer_genome_atlas_engine.schemas import CLUSTER_SUMMARY, EXPRESSION_CLUSTERS

INPUTS = ("expression_coordinates", "cases_diagnoses")
OUTPUTS = ("expression_clusters", "cluster_summary")


@dataclass(frozen=True)
class Params:
    """Parameters for the K-means clustering."""

    n_clusters: int = 4
    random_state: int = 42


def run(inputs: dict[str, pa.Table], params: Params) -> dict[str, pa.Table]:
    """Return the clustered samples with their diagnosis and the cluster-by-tissue summary."""
    joined = run_query(io.read_sql("expression_cluster_inputs"), inputs)
    rows = joined.to_pylist()
    if not rows:
        message = (
            "expression_clusters has no samples; check expression_coordinates and cases_diagnoses"
        )
        raise ValueError(message)
    if params.n_clusters < 1:
        message = f"Parameter n_clusters is {params.n_clusters}; it must be at least 1"
        raise ValueError(message)
    if params.n_clusters > len(rows):
        message = (
            f"Parameter n_clusters is {params.n_clusters}; "
            f"there are only {len(rows)} samples to cluster"
        )
        raise ValueError(message)

    points = np.array([[row["tsne_1"], row["tsne_2"]] for row in rows], dtype=float)
    kmeans = KMeans(n_clusters=params.n_clusters, random_state=params.random_state, n_init=10)
    labels = kmeans.fit_predict(points)

    clustered = [
        {**row, "kmeans_cluster": int(label)} for row, label in zip(rows, labels, strict=True)
    ]
    clusters = align(
        pa.Table.from_pylist(clustered, schema=EXPRESSION_CLUSTERS), EXPRESSION_CLUSTERS
    )
    summary = run_query(io.read_sql("cluster_summary"), {"expression_clusters": clusters})
    return {
        "expression_clusters": clusters,
        "cluster_summary": align(summary, CLUSTER_SUMMARY),
    }
