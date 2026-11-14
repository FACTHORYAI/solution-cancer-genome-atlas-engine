"""Join the cases to their sample files: exposures per sample."""

from __future__ import annotations

from dataclasses import dataclass

import pyarrow as pa

from cancer_genome_atlas_engine import io
from cancer_genome_atlas_engine.jobs._duck import align, run_query
from cancer_genome_atlas_engine.schemas import CASES_EXPOSURES

INPUTS = ("cases", "expression_files_info")
OUTPUTS = ("cases_exposures",)


@dataclass(frozen=True)
class Params:
    """Parameters for the exposures table."""


def run(inputs: dict[str, pa.Table], params: Params) -> dict[str, pa.Table]:
    """Return exposures with a smoking status, one row per sample file."""
    table = run_query(io.read_sql("cases_exposures"), inputs)
    return {"cases_exposures": align(table, CASES_EXPOSURES)}
