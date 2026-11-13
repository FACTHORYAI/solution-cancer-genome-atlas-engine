-- The size of the expression dataset the analysis works on.
SELECT count(DISTINCT file_id) AS samples,
       count(DISTINCT gene_id) AS genes,
       count(*) AS expression_rows
FROM expression_profiles
