-- How the samples distribute over smoking status.
SELECT smoking_status,
       count(DISTINCT file_id) AS samples
FROM cases_exposures
GROUP BY smoking_status
ORDER BY samples DESC, smoking_status
