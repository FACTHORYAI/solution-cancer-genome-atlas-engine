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

Cancer Genome Atlas Engine takes the open-access data of The Cancer Genome Atlas (TCGA), the clinical record of each cancer case and the RNA-Seq gene expression of its tissue samples, and turns it into tables that show how the samples relate: which genes vary most, how the samples sit next to each other in expression space, which of them cluster together and from which tissue, and how the cohort splits by tissue of origin, gender and vital status, and smoking status.

1. **Clean.** Three jobs clean the three tables of the raw data. File metadata and clinical cases without their identifiers are dropped, and a negative FPKM value in the expression profiles becomes missing.
2. **Join.** Three jobs join each case to its sample files: demographics with a vital-status flag, diagnoses with a treatment flag, and exposures with a smoking status.
3. **Select genes.** `select_variable_genes` ranks the genes by how much their expression varies across the samples and keeps the most variable ones.
4. **Reduce.** `expression_dimensions` standardises the samples-by-genes matrix and computes a PCA, with the variance each component explains, and a t-SNE map of the samples.
5. **Cluster.** `cluster_expression` groups the samples with K-means on their t-SNE coordinates and counts each cluster's samples by tissue of origin.
6. **Summarise the cohort.** Three SQL jobs count the samples by tissue of origin, by gender and vital status, and by smoking status.

It needs no language model: the cleaning, joins, rankings and counts are SQL on DuckDB, and the PCA, t-SNE and K-means are scikit-learn.

## How it works in Facthory

- Jobs read tables and write tables. They draw no screens and own no storage; querying, charting, joining with your own data, permissions and audit belong to the platform.
- The agent skill in `skills/` and the starter page in `pages/` describe how to work with the tables and the jobs.
- The sample data in this repository is a small real subset of de-identified open-access TCGA data from the Genomic Data Commons. It is not synthetic. See "Data" below.

## What the result could look like

![Mock-up of a Facthory report page titled "Patient similarity map", marked "Sample data": a scatter plot of 600 patients in two dimensions, labelled by tissue or organ of origin (liver, kidney, skin, prostate gland, endometrium, ovary, cerebrum, thyroid gland, breast, upper lobe of lung), with buttons to group by tissue or organ of origin, primary diagnosis or tumour grade, and a list of the groups with their patient counts.](docs/images/patient-similarity-map-mockup.png)

A design illustration of a similarity map: each dot is a patient, grouped by tissue or organ of origin, primary diagnosis or tumour grade. It is a mock-up. Its figures are illustrative: it shows 600 patients, not this repository's 9 samples, and it is not a screenshot of a released feature. Note that the mock-up's subtitle describes patients whose reports read alike; this repository draws its map from gene expression profiles (principal components and t-SNE), not from report text.

## Jobs

| Job | What it does | Inputs | Outputs |
| --- | --- | --- | --- |
| `clean_expression_files` | Cleans the file metadata, keeping files with both identifiers | `expression_files_info_raw` | `expression_files_info` |
| `clean_cases` | Cleans the clinical cases, keeping cases with a case identifier | `cases_raw` | `cases` |
| `clean_expression_profiles` | Cleans the expression profiles and validates their FPKM values | `expression_profiles_raw` | `expression_profiles` |
| `cases_demographics` | Joins cases to sample files: demographics, with vital status | `cases`, `expression_files_info` | `cases_demographics` |
| `cases_diagnoses` | Joins cases to sample files: diagnoses, with a treatment flag | `cases`, `expression_files_info` | `cases_diagnoses` |
| `cases_exposures` | Joins cases to sample files: exposures, with smoking status | `cases`, `expression_files_info` | `cases_exposures` |
| `select_variable_genes` | The genes whose expression varies most across samples | `expression_profiles` | `gene_variance` |
| `expression_dimensions` | PCA and t-SNE coordinates per sample, with explained variance | `expression_profiles`, `gene_variance` | `expression_coordinates`, `explained_variance` |
| `cluster_expression` | K-means clusters over the reduced samples, summarised by tissue | `expression_coordinates`, `cases_diagnoses` | `expression_clusters`, `cluster_summary` |
| `tissue_summary` | Samples per tissue of origin | `cases_diagnoses` | `tissue_summary` |
| `demographic_summary` | Samples per gender and vital status | `cases_demographics` | `demographic_summary` |
| `exposure_summary` | Samples per smoking status | `cases_exposures` | `exposure_summary` |

Every job is a plain function from named PyArrow tables to named tables: the joins, filters and aggregations run as DuckDB SQL (`src/cancer_genome_atlas_engine/sql/`), and the dimensionality reduction and clustering use scikit-learn. Named measures live in `metrics/`.

## Data

The sample tables in `data/sample/` are a small real subset of open-access data of The Cancer Genome Atlas (TCGA), published by the Genomic Data Commons (GDC): nine RNA-Seq samples (files) of seven cases from TCGA-BRCA, TCGA-LUAD and TCGA-KIRC over the 300 most variable genes, and the tables the jobs make from them. 17 files, about 280 KB. The data are de-identified, but they are real tumour samples with real clinical fields. They are not synthetic. Their licence is recorded as `LicenseRef-GDC-open-access`. See [data/README.md](data/README.md) for one row per file with its origin and licence.

The GDC puts two obligations on everyone who uses its open-access data, under the NIH Genomic Data Sharing policy:

- Acknowledge TCGA, the GDC and the datasets you used in publications and presentations.
- Make no attempt to identify the participants the data come from.

## Run it locally

```
uv sync
uv run python -m cancer_genome_atlas_engine expression_dimensions --n-pca-components 10
uv run python -m cancer_genome_atlas_engine cluster_expression --n-clusters 4
uv run pytest
```

`uv run python -m cancer_genome_atlas_engine --help` lists every job; each job has its own `--help`. A job reads the tables it names from `data/sample/` and writes its outputs as Parquet files into `output/`, which is not committed. The jobs run in order: the cleaning jobs first, then the joins, then `select_variable_genes`, `expression_dimensions` and `cluster_expression`; the summaries read the joined tables. Verified on the sample data on a laptop only, not yet in a Facthory workspace.

## Open points

- **The sample is real data, and the terms for redistributing it are under review.** It is a small real subset of de-identified open-access TCGA data, not a generated one. Whether this repository may redistribute the subset is not settled, and the subset may be replaced by a generated one. Until then, use it as TCGA data under the GDC's terms (see "Data").
- **The sample's clinical fields are real.** Gender, race, ethnicity, birth and death year, diagnosis, treatments and exposures are TCGA's recorded values for real people. This subset leaves many of them empty: gender is empty for every case, only one case has a birth year and one a recorded treatment, none has a death year or smoking data, and so `demographic_summary` and `exposure_summary` each return a single row.
- **The full TCGA release does not fit the platform's limits as is.** A dataset file is at most 256 MiB, and a code run gets at most 32 MiB of input, 120 seconds, 512 MiB of memory and one CPU. The jobs here read the expression table as one row per sample and gene and build the matrix in Python, which works for the sample only. At scale the analytics engine must first reduce the expression table to a sample-by-gene matrix of the most variable genes, and only that matrix goes to the Python steps. That reduction is not built or run yet. A t-SNE over thousands of samples probably exceeds a run's limits; this has not been measured.
- **Clustering is exploratory.** The clusters are an unsupervised K-means grouping of t-SNE coordinates. They depend on the number of clusters, the gene set and the seed, and distances in a t-SNE map carry little meaning. They are not a clinical classification. With nine samples, the map and the clusters show how the jobs work, not biology.
- **t-SNE values depend on the platform.** A run on another machine gives other t-SNE coordinates than the stored ones, and K-means follows them. PCA agrees to rounding error. The tests compare the PCA values with a tolerance, and for t-SNE only its shape and that one seed gives one result.
- **No text model is needed.** Every job is SQL on DuckDB or scikit-learn; nothing reads free text.
- **Installing into Facthory is not available yet.** The code is verified on the sample data on a laptop only.
- **The Dockerfile has not been built or verified.**
- **DuckDB 2.x only.** The code uses the DuckDB 2.0 Arrow API (`to_arrow_table`).

## Not for clinical use

This is software for research and analytics. It is not a medical device and must not be used to diagnose or treat a patient. Results can be wrong; a qualified person reviews them.

## Disclaimers

Bandpey GmbH (“Facthory”) does not dispense medical, diagnosis, or treatment advice. This Solution (“tool”) is for informational purposes only and may not be used as a substitute for professional medical advice, treatment, or diagnosis. This tool may not be used within Facthory to process Protected Health Information (“PHI”) as defined in the Health Insurance Portability and Accountability Act of 1996, unless you have executed with Facthory a contract that allows for processing PHI, an accompanying Business Associate Agreement (BAA), and are running this tool within a HIPAA Account.

## Licence

Apache-2.0. See [LICENSE](LICENSE). "Facthory" and the Facthory logo are trademarks of their owner and are not covered by that licence. This includes the logo shown in the image under `docs/images/`.
