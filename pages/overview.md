# Cancer Genome Atlas Engine

Analyse the open data of The Cancer Genome Atlas (TCGA) across cancer types.

## Start here

1. Look at the sample tables in `data/sample`: a small real TCGA open-access subset — nine RNA-Seq samples from three projects (breast, lung, kidney) over the 300 most variable genes.
2. Follow the pipeline: raw tables → silver (`expression_profiles`, `cases_demographics`, `cases_diagnoses`, `cases_exposures`) → gold (`gene_variance`, `expression_coordinates`, `expression_clusters`).
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

- The sample data is real TCGA open-access data from the GDC; acknowledge TCGA and the GDC when you use results.
- Clusters are an unsupervised grouping of expression profiles: exploratory, sensitive to the number of clusters and the gene set, and not a clinical classification.
- Results are for research and analytics, not clinical decisions.
