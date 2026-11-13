-- How each cluster is composed by tissue of origin.
SELECT kmeans_cluster,
       coalesce(tissue_or_organ_of_origin, '') AS tissue_or_organ_of_origin,
       count(*) AS samples
FROM expression_clusters
GROUP BY kmeans_cluster, tissue_or_organ_of_origin
ORDER BY kmeans_cluster, tissue_or_organ_of_origin
