"""How the samples distribute over smoking status."""

from __future__ import annotations

from dataclasses import dataclass

import pyarrow as pa

from cancer_genome_atlas_engine import io
from cancer_genome_atlas_engine.jobs._duck import align, run_query
from cancer_genome_atlas_engine.schemas import EXPOSURE_SUMMARY

INPUTS = ("cases_exposures",)
OUTPUTS = ("exposure_summary",)


@dataclass(frozen=True)
class Params:
    """Parameters for the exposure summary."""


def run(inputs: dict[str, pa.Table], params: Params) -> dict[str, pa.Table]:
    """Return the number of sample files per smoking status."""
    table = run_query(io.read_sql("exposure_summary"), inputs)
    return {"exposure_summary": align(table, EXPOSURE_SUMMARY)}
