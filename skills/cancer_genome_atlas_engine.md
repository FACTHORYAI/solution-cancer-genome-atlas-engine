# Cancer Genome Atlas Engine — agent instructions

You help members analyse TCGA open data: gene expression across cancer types, clinical cohorts, and the structure of the samples in expression space.

## What the project provides

- Sample tables in `data/sample` (a small real TCGA open-access subset from the GDC): raw `expression_files_info_raw`, `cases_raw`, `expression_profiles_raw`; the silver tables `expression_files_info`, `cases`, `expression_profiles`, `cases_demographics`, `cases_diagnoses`, `cases_exposures`; and the gold tables `gene_variance`, `expression_coordinates`, `explained_variance`, `expression_clusters`, `cluster_summary`.
- Jobs under `src/cancer_genome_atlas_engine/jobs`: six silver jobs (cleaning and joining raw data), three gold jobs (variable genes, PCA/t-SNE, K-means), and three cohort summaries.

## How to answer a question

1. Classify what the member asks: dataset size (`expression_profiles`), which genes vary most (`gene_variance`), how samples group in expression space (`expression_coordinates`, `expression_clusters`, `cluster_summary`), or the cohort composition (`tissue_summary`, `demographic_summary`, `exposure_summary`).
2. Check the parameters with `uv run python -m cancer_genome_atlas_engine <job> --help`; `limit` caps the genes kept, `n_pca_components` caps the components, `n_clusters` must not exceed the number of samples.
3. Run the job, or answer directly from the tables: `expression_profiles` holds one row per sample and gene with validated FPKM; `expression_coordinates` holds pc1–pc3 and t-SNE coordinates per sample; `expression_clusters` adds the tissue, diagnosis and cluster.
4. Report results as a table with the counts behind them. Never guess beyond the tables, and never present a cluster as a clinical grouping without saying it is an unsupervised grouping of expression profiles.

## Data care

- The sample data is real TCGA open-access data published by the GDC; cite TCGA and the GDC when results are used, and never mix in identifiable or controlled-access data.
- Expression clusters are exploratory: K-means over reduced expression profiles, sensitive to the number of clusters and the gene set.
- Results are for research and analytics, not clinical decisions.
