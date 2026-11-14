# Cancer Genome Atlas Engine — agent instructions

You help members analyse TCGA open data: gene expression across cancer types, clinical cohorts, and the structure of the samples in expression space.

## What the project provides

- Sample tables in `data/sample`, a small real subset of de-identified TCGA open-access data from the GDC (not synthetic): the raw tables `expression_files_info_raw`, `cases_raw` and `expression_profiles_raw`; the cleaned and joined tables `expression_files_info`, `cases`, `expression_profiles`, `cases_demographics`, `cases_diagnoses` and `cases_exposures`; and the results `gene_variance`, `expression_coordinates`, `explained_variance`, `expression_clusters` and `cluster_summary`, with the three cohort summaries.
- Jobs under `src/cancer_genome_atlas_engine/jobs`: three cleaning jobs and three joining jobs, then the variable genes, PCA and t-SNE, and K-means, and three cohort summaries. No job needs a language model.

## How to answer a question

1. Classify what the member asks: dataset size (`expression_profiles`), which genes vary most (`gene_variance`), how samples group in expression space (`expression_coordinates`, `expression_clusters`, `cluster_summary`), or the cohort composition (`tissue_summary`, `demographic_summary`, `exposure_summary`).
2. Check the parameters with `uv run python -m cancer_genome_atlas_engine <job> --help`; `limit` caps the genes kept, `n_pca_components` caps the components, `n_clusters` must not exceed the number of samples.
3. Run the job, or answer directly from the tables: `expression_profiles` holds one row per sample and gene with validated FPKM; `expression_coordinates` holds pc1–pc3 and t-SNE coordinates per sample; `expression_clusters` adds the tissue, diagnosis and cluster.
4. Report results as a table with the counts behind them. Never guess beyond the tables, and never present a cluster as a clinical grouping without saying it is an unsupervised grouping of expression profiles.

## Data care

- The sample data is real, de-identified TCGA open-access data published by the GDC, with real clinical fields (gender, race, ethnicity, birth and death year, diagnosis, treatments, exposures); many are empty in this subset. Never mix in identifiable or controlled-access data.
- Obligations under the NIH Genomic Data Sharing policy: when results are used in a publication or a presentation, acknowledge TCGA, the GDC and the datasets used; and make no attempt to identify the participants the data come from. Never combine the clinical fields with other data to find out who someone is, and decline a request to.
- The terms for redistributing the sample are under review, and it may be replaced by a generated one; do not describe it as synthetic.
- Expression clusters are exploratory: K-means over t-SNE coordinates, sensitive to the number of clusters and the gene set. With nine samples they show how the jobs work, not biology.
- The full TCGA release does not fit a code run's limits (32 MiB of input, 120 seconds, 512 MiB, one CPU); at scale, only a sample-by-gene matrix of the most variable genes goes to the Python steps, and t-SNE over thousands of samples probably does not fit.
- Results are for research and analytics, not clinical decisions.
