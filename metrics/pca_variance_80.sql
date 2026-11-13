-- How many principal components it takes to explain 80% of the expression variance.
SELECT min(component) AS components_for_80_percent
FROM explained_variance
WHERE cumulative_variance >= 0.8
