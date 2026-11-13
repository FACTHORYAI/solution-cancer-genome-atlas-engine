-- How the samples distribute over gender and vital status.
SELECT coalesce(gender, '') AS gender,
       CASE WHEN is_deceased THEN 'Deceased' ELSE 'Alive' END AS vital_status,
       count(DISTINCT file_id) AS samples
FROM cases_demographics
GROUP BY gender, vital_status
ORDER BY samples DESC, gender, vital_status
