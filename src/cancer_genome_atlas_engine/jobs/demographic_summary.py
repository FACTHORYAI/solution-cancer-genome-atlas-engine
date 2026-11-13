"""How the samples distribute over gender and vital status."""

from __future__ import annotations

from dataclasses import dataclass

import pyarrow as pa

from cancer_genome_atlas_engine import io
from cancer_genome_atlas_engine.jobs._duck import align, run_query
from cancer_genome_atlas_engine.schemas import DEMOGRAPHIC_SUMMARY

INPUTS = ("cases_demographics",)
OUTPUTS = ("demographic_summary",)


@dataclass(frozen=True)
class Params:
    """Parameters for the demographic summary."""


def run(inputs: dict[str, pa.Table], params: Params) -> dict[str, pa.Table]:
    """Return the number of sample files per gender and vital status."""
    table = run_query(io.read_sql("demographic_summary"), inputs)
    return {"demographic_summary": align(table, DEMOGRAPHIC_SUMMARY)}
