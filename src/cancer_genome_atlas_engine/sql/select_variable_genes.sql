-- The genes whose expression varies most across the samples: the feature set for the
-- dimensionality reduction. $limit caps how many genes are kept.
SELECT gene_id,
       max(gene_name) AS gene_name,
       var_samp(fpkm_unstranded_validated) AS variance,
       avg(fpkm_unstranded_validated) AS mean_expression,
       count(fpkm_unstranded_validated) AS samples
FROM expression_profiles
WHERE fpkm_unstranded_validated IS NOT NULL
GROUP BY gene_id
HAVING count(fpkm_unstranded_validated) >= 2
ORDER BY variance DESC, gene_id
LIMIT $limit
