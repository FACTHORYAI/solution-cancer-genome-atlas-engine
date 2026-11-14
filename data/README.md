# Sample data

A small, real subset of **TCGA open-access data** from The Cancer Genome Atlas, published by
the [Genomic Data Commons (GDC)](https://gdc.cancer.gov/): nine RNA-Seq samples (files) of
seven cases from three TCGA projects (TCGA-BRCA, TCGA-LUAD, TCGA-KIRC), reduced to the 300
most variable expressed genes so the whole folder stays small, and the tables the jobs make from
them. **None of it is synthetic.** The data are de-identified, but they are real tumour samples
with real clinical fields: gender, race, ethnicity, birth and death year, diagnosis, treatments
and exposures. This subset leaves many of those empty (gender is empty for every case; one case
has a birth year and one a recorded treatment; none has a death year or smoking data).

**Provenance.** Fetched from the GDC API (`/files`, `/cases`, `/data`) with the filters
`data_type = Gene Expression Quantification`, `experimental_strategy = RNA-Seq`,
`access = open`. The gene set is the 300 most variable genes across these samples with
mean FPKM above 1.

**Licence.** TCGA open-access data can be used without applying for access, under the GDC's
data-use terms and the NIH Genomic Data Sharing policy. No SPDX identifier exists for those
terms, so every file's licence is the reference `LicenseRef-GDC-open-access`, and `synthetic`
is `false` in `facthory.toml`. The terms for redistributing this subset in this repository are
under review, and the subset may be replaced by a generated one.

**What the GDC asks of everyone who uses these data**, under the NIH Genomic Data Sharing policy:

- Acknowledge TCGA, the GDC and the datasets used in publications and presentations.
- Make no attempt to identify the participants the data come from.

| File | What it is | Where it came from | Licence | Synthetic |
| --- | --- | --- | --- | --- |
| `expression_files_info_raw.parquet` | File metadata per sample file: file, case, project, name, size, format, strategy, sample type | GDC `/files` | `LicenseRef-GDC-open-access` | no |
| `cases_raw.parquet` | Clinical record per case: demographics, diagnosis, treatments, exposures | GDC `/cases` | `LicenseRef-GDC-open-access` | no |
| `expression_profiles_raw.parquet` | Gene expression values per sample and gene: counts, TPM, FPKM | GDC `/data` | `LicenseRef-GDC-open-access` | no |
| `expression_files_info.parquet` | The file metadata, cleaned: files with both identifiers | `clean_expression_files` | `LicenseRef-GDC-open-access` | no |
| `cases.parquet` | The clinical cases, cleaned: cases with a case identifier | `clean_cases` | `LicenseRef-GDC-open-access` | no |
| `expression_profiles.parquet` | The expression profiles, cleaned, with validated FPKM values | `clean_expression_profiles` | `LicenseRef-GDC-open-access` | no |
| `cases_demographics.parquet` | Demographics per sample, with vital status | `cases_demographics` | `LicenseRef-GDC-open-access` | no |
| `cases_diagnoses.parquet` | Diagnoses per sample, with a treatment flag | `cases_diagnoses` | `LicenseRef-GDC-open-access` | no |
| `cases_exposures.parquet` | Exposures per sample, with smoking status | `cases_exposures` | `LicenseRef-GDC-open-access` | no |
| `gene_variance.parquet` | The 300 most variable genes with variance and mean expression | `select_variable_genes` | `LicenseRef-GDC-open-access` | no |
| `expression_coordinates.parquet` | PCA and t-SNE coordinates per sample | `expression_dimensions` | `LicenseRef-GDC-open-access` | no |
| `explained_variance.parquet` | Variance explained by each principal component | `expression_dimensions` | `LicenseRef-GDC-open-access` | no |
| `expression_clusters.parquet` | K-means cluster per sample with its diagnosis | `cluster_expression` | `LicenseRef-GDC-open-access` | no |
| `cluster_summary.parquet` | Cluster composition by tissue of origin | `cluster_expression` | `LicenseRef-GDC-open-access` | no |
| `tissue_summary.parquet` | Samples per tissue of origin | `tissue_summary` | `LicenseRef-GDC-open-access` | no |
| `demographic_summary.parquet` | Samples per gender and vital status | `demographic_summary` | `LicenseRef-GDC-open-access` | no |
| `exposure_summary.parquet` | Samples per smoking status | `exposure_summary` | `LicenseRef-GDC-open-access` | no |

The first three files are the data as fetched; every other file is made from them by the job
named in its row, so the folder holds each job's expected output on the sample. The folder is
about 280 KB, far under the limit of 5 MB per file.

The t-SNE columns of `expression_coordinates.parquet`, and the clusters in
`expression_clusters.parquet` and `cluster_summary.parquet` that follow from them, depend on
the maths libraries of the machine that made them: running the jobs elsewhere gives other
values. The PCA columns and `explained_variance.parquet` reproduce to rounding error.
