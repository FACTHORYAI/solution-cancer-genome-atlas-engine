-- How many samples each tissue of origin contributes.
SELECT coalesce(tissue_or_organ_of_origin, '') AS tissue_or_organ_of_origin,
       count(DISTINCT file_id) AS samples
FROM cases_diagnoses
GROUP BY tissue_or_organ_of_origin
ORDER BY samples DESC, tissue_or_organ_of_origin
