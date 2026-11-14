"""Clean the clinical cases: keep the cases that carry a case identifier."""

from __future__ import annotations

from dataclasses import dataclass

import pyarrow as pa

from cancer_genome_atlas_engine import io
from cancer_genome_atlas_engine.jobs._duck import align, run_query
from cancer_genome_atlas_engine.schemas import CASES

INPUTS = ("cases_raw",)
OUTPUTS = ("cases",)


@dataclass(frozen=True)
class Params:
    """Parameters for the case cleaning."""


def run(inputs: dict[str, pa.Table], params: Params) -> dict[str, pa.Table]:
    """Return the clinical case rows that carry a case identifier."""
    table = run_query(io.read_sql("clean_cases"), inputs)
    return {"cases": align(table, CASES)}
