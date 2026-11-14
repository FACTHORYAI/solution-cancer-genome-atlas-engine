# Cancer Genome Atlas Engine

Analyse the open data of The Cancer Genome Atlas (TCGA) across cancer types.

## Start here

1. Look at the sample tables in `data/sample`: a small real TCGA open-access subset — nine RNA-Seq samples from three projects (breast, lung, kidney) over the 300 most variable genes.
2. Follow the jobs: the raw tables are cleaned (`expression_profiles`) and joined per sample (`cases_demographics`, `cases_diagnoses`, `cases_exposures`), then analysed (`gene_variance`, `expression_coordinates`, `expression_clusters`).
3. Ask a question and run its job:

| Question | Job |
| --- | --- |
| Which genes vary most across the samples? | `select_variable_genes` |
| How do the samples arrange in expression space? | `expression_dimensions` |
| Which samples cluster together, and by tissue? | `cluster_expression` |
| Which tissues contribute how many samples? | `tissue_summary` |
| How does the cohort split by gender and vital status? | `demographic_summary` |
| How does the cohort split by smoking status? | `exposure_summary` |

Named measures for dataset size and PCA variance live in `metrics/`.

## Notes

- The sample data is real, de-identified TCGA open-access data from the GDC, not synthetic. Acknowledge TCGA, the GDC and the datasets used in publications and presentations, and make no attempt to identify participants.
- The terms for redistributing the sample are under review, and it may be replaced by a generated one.
- The jobs need no language model.
- Clusters are an unsupervised grouping of expression profiles: exploratory, sensitive to the number of clusters and the gene set, and not a clinical classification.
- Results are for research and analytics, not clinical decisions.
