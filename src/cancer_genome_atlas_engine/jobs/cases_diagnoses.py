"""Join the cases to their sample files: diagnoses per sample."""

from __future__ import annotations

from dataclasses import dataclass

import pyarrow as pa

from cancer_genome_atlas_engine import io
from cancer_genome_atlas_engine.jobs._duck import align, run_query
from cancer_genome_atlas_engine.schemas import CASES_DIAGNOSES

INPUTS = ("cases", "expression_files_info")
OUTPUTS = ("cases_diagnoses",)


@dataclass(frozen=True)
class Params:
    """Parameters for the diagnoses table."""


def run(inputs: dict[str, pa.Table], params: Params) -> dict[str, pa.Table]:
    """Return diagnoses with a treatment flag, one row per sample file."""
    table = run_query(io.read_sql("cases_diagnoses"), inputs)
    return {"cases_diagnoses": align(table, CASES_DIAGNOSES)}
