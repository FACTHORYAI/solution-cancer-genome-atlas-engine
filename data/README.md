# Sample data

A small, real subset of **TCGA open-access data**, published by the
[Genomic Data Commons (GDC)](https://gdc.cancer.gov/). Nine RNA-Seq samples from three
TCGA projects (TCGA-BRCA, TCGA-LUAD, TCGA-KIRC), reduced to the 300 most variable
expressed genes so the whole folder stays small.

**Provenance.** Fetched from the GDC API (`/files`, `/cases`, `/data`) with the filters
`data_type = Gene Expression Quantification`, `experimental_strategy = RNA-Seq`,
`access = open`. The gene set is the 300 most variable genes across these samples with
mean FPKM above 1.

**Licence and attribution.** TCGA open-access data are free to use; NCI asks users to
acknowledge TCGA and the GDC in publications. The data are de-identified; no identifiable
patient data is present.

| File | What it is | Origin | Licence |
| --- | --- | --- | --- |
| `expression_files_info_raw.parquet` | File metadata per sample (file, case, project, size, format, sample type) | GDC `/files` | TCGA open access |
| `cases_raw.parquet` | Clinical record per case (demographics, diagnosis, treatments, exposures) | GDC `/cases` | TCGA open access |
| `expression_profiles_raw.parquet` | Gene expression values per sample and gene (counts, TPM, FPKM) | GDC `/data` | TCGA open access |
| `expression_files_info.parquet` | Silver: file metadata with both identifiers present | `clean_expression_files` | TCGA open access |
| `cases.parquet` | Silver: clinical cases with a case identifier | `clean_cases` | TCGA open access |
| `expression_profiles.parquet` | Silver: expression profiles with validated FPKM values | `clean_expression_profiles` | TCGA open access |
| `cases_demographics.parquet` | Silver: demographics per sample, with vital status | `cases_demographics` | TCGA open access |
| `cases_diagnoses.parquet` | Silver: diagnoses per sample, with treatment flag | `cases_diagnoses` | TCGA open access |
| `cases_exposures.parquet` | Silver: exposures per sample, with smoking status | `cases_exposures` | TCGA open access |
| `gene_variance.parquet` | The 300 most variable genes with variance and mean expression | `select_variable_genes` | TCGA open access |
| `expression_coordinates.parquet` | PCA and t-SNE coordinates per sample | `expression_dimensions` | TCGA open access |
| `explained_variance.parquet` | Variance explained by each principal component | `expression_dimensions` | TCGA open access |
| `expression_clusters.parquet` | K-means cluster per sample with its diagnosis | `cluster_expression` | TCGA open access |
| `cluster_summary.parquet` | Cluster composition by tissue of origin | `cluster_expression` | TCGA open access |
| `tissue_summary.parquet` | Samples per tissue of origin | `tissue_summary` | TCGA open access |
| `demographic_summary.parquet` | Samples per gender and vital status | `demographic_summary` | TCGA open access |
| `exposure_summary.parquet` | Samples per smoking status | `exposure_summary` | TCGA open access |

Every file is well under the 5 MB limit; the whole folder is about 250 KB.

A workspace run points the same jobs at the full TCGA release through Facthory's own
storage; the sample only demonstrates the pipeline.
