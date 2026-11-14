"""Clean the file metadata: keep the files that carry both a file and a case identifier."""

from __future__ import annotations

from dataclasses import dataclass

import pyarrow as pa

from cancer_genome_atlas_engine import io
from cancer_genome_atlas_engine.jobs._duck import align, run_query
from cancer_genome_atlas_engine.schemas import EXPRESSION_FILES_INFO

INPUTS = ("expression_files_info_raw",)
OUTPUTS = ("expression_files_info",)


@dataclass(frozen=True)
class Params:
    """Parameters for the expression-file cleaning."""


def run(inputs: dict[str, pa.Table], params: Params) -> dict[str, pa.Table]:
    """Return the file metadata rows that carry both a file and a case identifier."""
    table = run_query(io.read_sql("clean_expression_files"), inputs)
    return {"expression_files_info": align(table, EXPRESSION_FILES_INFO)}
