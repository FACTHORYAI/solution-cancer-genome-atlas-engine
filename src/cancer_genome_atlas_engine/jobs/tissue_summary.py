"""How many samples each tissue of origin contributes."""

from __future__ import annotations

from dataclasses import dataclass

import pyarrow as pa

from cancer_genome_atlas_engine import io
from cancer_genome_atlas_engine.jobs._duck import align, run_query
from cancer_genome_atlas_engine.schemas import TISSUE_SUMMARY

INPUTS = ("cases_diagnoses",)
OUTPUTS = ("tissue_summary",)


@dataclass(frozen=True)
class Params:
    """Parameters for the tissue summary."""


def run(inputs: dict[str, pa.Table], params: Params) -> dict[str, pa.Table]:
    """Return the number of sample files per tissue of origin."""
    table = run_query(io.read_sql("tissue_summary"), inputs)
    return {"tissue_summary": align(table, TISSUE_SUMMARY)}
