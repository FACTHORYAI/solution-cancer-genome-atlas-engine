"""PyArrow schemas for every table the jobs read or write."""

import pyarrow as pa

EXPRESSION_FILES_INFO_RAW = pa.schema(
    [
        pa.field("file_id", pa.string()),
        pa.field("case_id", pa.string()),
        pa.field("project_id", pa.string()),
        pa.field("file_name", pa.string()),
        pa.field("file_size", pa.int64()),
        pa.field("data_format", pa.string()),
        pa.field("experimental_strategy", pa.string()),
        pa.field("sample_type", pa.string()),
    ]
)

EXPRESSION_FILES_INFO = pa.schema(
    [
        pa.field("file_id", pa.string()),
        pa.field("case_id", pa.string()),
        pa.field("project_id", pa.string()),
        pa.field("file_size", pa.int64()),
        pa.field("data_format", pa.string()),
        pa.field("sample_type", pa.string()),
    ]
)

CASES = pa.schema(
    [
        pa.field("case_id", pa.string()),
        pa.field("gender", pa.string()),
        pa.field("race", pa.string()),
        pa.field("ethnicity", pa.string()),
        pa.field("year_of_birth", pa.int32()),
        pa.field("year_of_death", pa.int32()),
        pa.field("vital_status", pa.string()),
        pa.field("primary_diagnosis", pa.string()),
        pa.field("tissue_or_organ_of_origin", pa.string()),
        pa.field("tumor_grade", pa.string()),
        pa.field("classification_of_tumor", pa.string()),
        pa.field("treatments", pa.string()),
        pa.field("alcohol_history", pa.string()),
        pa.field("cigarettes_per_day", pa.float64()),
        pa.field("bmi", pa.float64()),
    ]
)

CASES_DEMOGRAPHICS = pa.schema(
    [
        pa.field("case_id", pa.string()),
        pa.field("file_id", pa.string()),
        pa.field("gender", pa.string()),
        pa.field("race", pa.string()),
        pa.field("ethnicity", pa.string()),
        pa.field("year_of_birth", pa.int32()),
        pa.field("year_of_death", pa.int32()),
        pa.field("is_deceased", pa.bool_()),
    ]
)

CASES_DIAGNOSES = pa.schema(
    [
        pa.field("case_id", pa.string()),
        pa.field("file_id", pa.string()),
        pa.field("classification_of_tumor", pa.string()),
        pa.field("primary_diagnosis", pa.string()),
        pa.field("tissue_or_organ_of_origin", pa.string()),
        pa.field("tumor_grade", pa.string()),
        pa.field("has_treatment", pa.bool_()),
    ]
)

CASES_EXPOSURES = pa.schema(
    [
        pa.field("case_id", pa.string()),
        pa.field("file_id", pa.string()),
        pa.field("alcohol_history", pa.string()),
        pa.field("cigarettes_per_day", pa.float64()),
        pa.field("bmi", pa.float64()),
        pa.field("smoking_status", pa.string()),
    ]
)

EXPRESSION_PROFILES_RAW = pa.schema(
    [
        pa.field("file_id", pa.string()),
        pa.field("gene_id", pa.string()),
        pa.field("gene_name", pa.string()),
        pa.field("gene_type", pa.string()),
        pa.field("unstranded", pa.int64()),
        pa.field("stranded_first", pa.float64()),
        pa.field("stranded_second", pa.float64()),
        pa.field("tpm_unstranded", pa.float64()),
        pa.field("fpkm_unstranded", pa.float64()),
        pa.field("fpkm_uq_unstranded", pa.float64()),
    ]
)

EXPRESSION_PROFILES = pa.schema(
    [
        pa.field("file_id", pa.string()),
        pa.field("gene_id", pa.string()),
        pa.field("gene_name", pa.string()),
        pa.field("gene_type", pa.string()),
        pa.field("unstranded", pa.int64()),
        pa.field("stranded_first", pa.float64()),
        pa.field("stranded_second", pa.float64()),
        pa.field("tpm_unstranded", pa.float64()),
        pa.field("fpkm_unstranded", pa.float64()),
        pa.field("fpkm_uq_unstranded", pa.float64()),
        pa.field("fpkm_unstranded_validated", pa.float64()),
    ]
)

GENE_VARIANCE = pa.schema(
    [
        pa.field("gene_id", pa.string()),
        pa.field("gene_name", pa.string()),
        pa.field("variance", pa.float64()),
        pa.field("mean_expression", pa.float64()),
        pa.field("samples", pa.int64()),
    ]
)

EXPRESSION_COORDINATES = pa.schema(
    [
        pa.field("file_id", pa.string()),
        pa.field("pc1", pa.float64()),
        pa.field("pc2", pa.float64()),
        pa.field("pc3", pa.float64()),
        pa.field("tsne_1", pa.float64()),
        pa.field("tsne_2", pa.float64()),
    ]
)

EXPLAINED_VARIANCE = pa.schema(
    [
        pa.field("component", pa.int32()),
        pa.field("explained_variance_ratio", pa.float64()),
        pa.field("cumulative_variance", pa.float64()),
    ]
)

EXPRESSION_CLUSTERS = pa.schema(
    [
        pa.field("file_id", pa.string()),
        pa.field("pc1", pa.float64()),
        pa.field("pc2", pa.float64()),
        pa.field("pc3", pa.float64()),
        pa.field("tsne_1", pa.float64()),
        pa.field("tsne_2", pa.float64()),
        pa.field("tissue_or_organ_of_origin", pa.string()),
        pa.field("primary_diagnosis", pa.string()),
        pa.field("tumor_grade", pa.string()),
        pa.field("kmeans_cluster", pa.int32()),
    ]
)

CLUSTER_SUMMARY = pa.schema(
    [
        pa.field("kmeans_cluster", pa.int32()),
        pa.field("tissue_or_organ_of_origin", pa.string()),
        pa.field("samples", pa.int64()),
    ]
)

TISSUE_SUMMARY = pa.schema(
    [
        pa.field("tissue_or_organ_of_origin", pa.string()),
        pa.field("samples", pa.int64()),
    ]
)

DEMOGRAPHIC_SUMMARY = pa.schema(
    [
        pa.field("gender", pa.string()),
        pa.field("vital_status", pa.string()),
        pa.field("samples", pa.int64()),
    ]
)

EXPOSURE_SUMMARY = pa.schema(
    [
        pa.field("smoking_status", pa.string()),
        pa.field("samples", pa.int64()),
    ]
)
