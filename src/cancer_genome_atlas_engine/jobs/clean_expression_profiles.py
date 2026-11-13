"""Silver: gene expression profiles with validated FPKM values."""

from __future__ import annotations

from dataclasses import dataclass

import pyarrow as pa

from cancer_genome_atlas_engine import io
from cancer_genome_atlas_engine.jobs._duck import align, run_query
from cancer_genome_atlas_engine.schemas import EXPRESSION_PROFILES

INPUTS = ("expression_profiles_raw",)
OUTPUTS = ("expression_profiles",)


@dataclass(frozen=True)
class Params:
    """Parameters for the expression-profile cleaning."""


def run(inputs: dict[str, pa.Table], params: Params) -> dict[str, pa.Table]:
    """Return the expression profiles with negative FPKM values replaced by null."""
    table = run_query(io.read_sql("clean_expression_profiles"), inputs)
    return {"expression_profiles": align(table, EXPRESSION_PROFILES)}
