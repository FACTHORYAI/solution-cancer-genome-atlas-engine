<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/FACTHORYAI/.github/main/brand/word-mark-only-mono.svg">
    <img alt="Facthory" src="https://raw.githubusercontent.com/FACTHORYAI/.github/main/brand/word-mark-only.svg" width="360">
  </picture>
</p>

# Cancer Genome Atlas Engine

Analyse the open data of The Cancer Genome Atlas (TCGA) across cancer types, in Facthory.

![Licence: Apache-2.0](https://img.shields.io/badge/licence-Apache--2.0-blue) ![Runs on Facthory](https://img.shields.io/badge/runs%20on-Facthory-1f6feb) ![Status: install coming](https://img.shields.io/badge/status-install%20coming-lightgrey)

> **Install coming.** This is a Facthory solution: its data, analysis code, agent skill and starting pages load into a Facthory workspace as a ready project. Installing from this page is not available yet; this repository is being prepared for it.

## What it does

Analyse the open data of The Cancer Genome Atlas (TCGA) across cancer types, in Facthory.

## How it will work in Facthory

- You install it into a workspace and get a project: sample data, the analysis, the agent's instructions and starting pages.
- Its results are tables and pages in your workspace, so you can query them, chart them and ask the agent about them, inside your permissions.
- Sample data in this repository is synthetic or openly licensed. No real patient data.

## What the result could look like

![Mock-up of a Facthory report page titled "Patient similarity map", marked "Sample data": a scatter plot of 600 patients in two dimensions, labelled by tissue or organ of origin (liver, kidney, skin, prostate gland, endometrium, ovary, cerebrum, thyroid gland, breast, upper lobe of lung), with buttons to group by tissue or organ of origin, primary diagnosis or tumour grade, and a list of the groups with their patient counts.](docs/images/patient-similarity-map-mockup.png)

A design illustration of a similarity map: each dot is a patient, grouped by tissue or organ of origin, primary diagnosis or tumour grade. It is a mock-up. Its figures are illustrative: it shows 600 patients, not this repository's 9 samples, and it is not a screenshot of a released feature. Note that the mock-up's subtitle describes patients whose reports read alike; this repository draws its map from gene expression profiles (principal components and t-SNE), not from report text.

## Not for clinical use

This is software for research and analytics. It is not a medical device and must not be used to diagnose or treat a patient. Results can be wrong; a qualified person reviews them.

## Licence

Apache-2.0. See [LICENSE](LICENSE). "Facthory" and the Facthory logo are trademarks of their owner and are not covered by that licence. This includes the logo shown in the image under `docs/images/`.

## Jobs

| Job | What it does | Inputs | Outputs |
| --- | --- | --- | --- |
| `clean_expression_files` | Silver: file metadata with both identifiers present | `expression_files_info_raw` | `expression_files_info` |
| `clean_cases` | Silver: clinical cases with a case identifier | `cases_raw` | `cases` |
| `clean_expression_profiles` | Silver: expression profiles with validated FPKM values | `expression_profiles_raw` | `expression_profiles` |
| `cases_demographics` | Silver: demographics per sample, with vital status | `cases`, `expression_files_info` | `cases_demographics` |
| `cases_diagnoses` | Silver: diagnoses per sample, with treatment flag | `cases`, `expression_files_info` | `cases_diagnoses` |
| `cases_exposures` | Silver: exposures per sample, with smoking status | `cases`, `expression_files_info` | `cases_exposures` |
| `select_variable_genes` | The genes whose expression varies most across samples | `expression_profiles` | `gene_variance` |
| `expression_dimensions` | PCA and t-SNE coordinates per sample, with explained variance | `expression_profiles`, `gene_variance` | `expression_coordinates`, `explained_variance` |
| `cluster_expression` | K-means clusters over the reduced samples, summarised by tissue | `expression_coordinates`, `cases_diagnoses` | `expression_clusters`, `cluster_summary` |
| `tissue_summary` | Samples per tissue of origin | `cases_diagnoses` | `tissue_summary` |
| `demographic_summary` | Samples per gender and vital status | `cases_demographics` | `demographic_summary` |
| `exposure_summary` | Samples per smoking status | `cases_exposures` | `exposure_summary` |

Every job is a plain function from named PyArrow tables to named tables: the joins, filters and aggregations run as DuckDB SQL (`sql/`), and the dimensionality reduction and clustering use scikit-learn. Named measures live in `metrics/`.

## Data

The sample tables in `data/sample/` are a small real subset of TCGA open-access data published by the Genomic Data Commons: nine RNA-Seq samples from TCGA-BRCA, TCGA-LUAD and TCGA-KIRC over the 300 most variable genes. See [data/README.md](data/README.md) for one row per file with origin and licence. TCGA open-access data are free to use; acknowledge TCGA and the GDC when you publish results.

## Run it locally

```
uv sync
uv run python -m cancer_genome_atlas_engine expression_dimensions --n-pca-components 10
uv run python -m cancer_genome_atlas_engine cluster_expression --n-clusters 4
uv run pytest
```

`uv run python -m cancer_genome_atlas_engine --help` lists every job; each job has its own `--help`. The pipeline runs layer by layer: the silver jobs clean the raw tables, `select_variable_genes` picks the feature set, `expression_dimensions` reduces it, and `cluster_expression` groups the samples; the summaries read the silver tables directly.

Clusters are an unsupervised grouping of expression profiles: exploratory, sensitive to the number of clusters and the gene set, and not a clinical classification.

