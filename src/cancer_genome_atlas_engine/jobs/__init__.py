"""The jobs of this solution: plain functions from named tables to named tables."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

import pyarrow as pa

from cancer_genome_atlas_engine.jobs import (
    cases_demographics,
    cases_diagnoses,
    cases_exposures,
    clean_cases,
    clean_expression_files,
    clean_expression_profiles,
    cluster_expression,
    demographic_summary,
    exposure_summary,
    expression_dimensions,
    select_variable_genes,
    tissue_summary,
)


@dataclass(frozen=True)
class JobSpec:
    """One job: its callable, its parameter class and its input and output tables."""

    name: str
    description: str
    run: Callable[..., dict[str, pa.Table]]
    params_cls: type
    inputs: tuple[str, ...]
    outputs: tuple[str, ...]


REGISTRY: dict[str, JobSpec] = {
    spec.name: spec
    for spec in (
        JobSpec(
            name="clean_expression_files",
            description="Cleans the file metadata, keeping files with both identifiers.",
            run=clean_expression_files.run,
            params_cls=clean_expression_files.Params,
            inputs=clean_expression_files.INPUTS,
            outputs=clean_expression_files.OUTPUTS,
        ),
        JobSpec(
            name="clean_cases",
            description="Cleans the clinical cases, keeping cases with a case identifier.",
            run=clean_cases.run,
            params_cls=clean_cases.Params,
            inputs=clean_cases.INPUTS,
            outputs=clean_cases.OUTPUTS,
        ),
        JobSpec(
            name="clean_expression_profiles",
            description="Cleans the expression profiles and validates their FPKM values.",
            run=clean_expression_profiles.run,
            params_cls=clean_expression_profiles.Params,
            inputs=clean_expression_profiles.INPUTS,
            outputs=clean_expression_profiles.OUTPUTS,
        ),
        JobSpec(
            name="cases_demographics",
            description="Joins cases to sample files: demographics, with vital status.",
            run=cases_demographics.run,
            params_cls=cases_demographics.Params,
            inputs=cases_demographics.INPUTS,
            outputs=cases_demographics.OUTPUTS,
        ),
        JobSpec(
            name="cases_diagnoses",
            description="Joins cases to sample files: diagnoses, with a treatment flag.",
            run=cases_diagnoses.run,
            params_cls=cases_diagnoses.Params,
            inputs=cases_diagnoses.INPUTS,
            outputs=cases_diagnoses.OUTPUTS,
        ),
        JobSpec(
            name="cases_exposures",
            description="Joins cases to sample files: exposures, with smoking status.",
            run=cases_exposures.run,
            params_cls=cases_exposures.Params,
            inputs=cases_exposures.INPUTS,
            outputs=cases_exposures.OUTPUTS,
        ),
        JobSpec(
            name="select_variable_genes",
            description="The genes whose expression varies most across the samples.",
            run=select_variable_genes.run,
            params_cls=select_variable_genes.Params,
            inputs=select_variable_genes.INPUTS,
            outputs=select_variable_genes.OUTPUTS,
        ),
        JobSpec(
            name="expression_dimensions",
            description="PCA and t-SNE coordinates per sample, with explained variance.",
            run=expression_dimensions.run,
            params_cls=expression_dimensions.Params,
            inputs=expression_dimensions.INPUTS,
            outputs=expression_dimensions.OUTPUTS,
        ),
        JobSpec(
            name="cluster_expression",
            description="K-means clusters over the reduced samples, summarised by tissue.",
            run=cluster_expression.run,
            params_cls=cluster_expression.Params,
            inputs=cluster_expression.INPUTS,
            outputs=cluster_expression.OUTPUTS,
        ),
        JobSpec(
            name="tissue_summary",
            description="How many samples each tissue of origin contributes.",
            run=tissue_summary.run,
            params_cls=tissue_summary.Params,
            inputs=tissue_summary.INPUTS,
            outputs=tissue_summary.OUTPUTS,
        ),
        JobSpec(
            name="demographic_summary",
            description="How the samples distribute over gender and vital status.",
            run=demographic_summary.run,
            params_cls=demographic_summary.Params,
            inputs=demographic_summary.INPUTS,
            outputs=demographic_summary.OUTPUTS,
        ),
        JobSpec(
            name="exposure_summary",
            description="How the samples distribute over smoking status.",
            run=exposure_summary.run,
            params_cls=exposure_summary.Params,
            inputs=exposure_summary.INPUTS,
            outputs=exposure_summary.OUTPUTS,
        ),
    )
}


def param_values(spec: JobSpec, args: Any) -> Any:
    """Build the job's Params instance from parsed command-line arguments."""
    values = {
        field.name: getattr(args, field.name)
        for field in spec.params_cls.__dataclass_fields__.values()
    }
    return spec.params_cls(**values)
