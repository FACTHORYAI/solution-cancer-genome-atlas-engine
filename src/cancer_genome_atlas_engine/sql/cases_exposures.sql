-- Silver: patient exposures with a smoking status, one row per sample file.
SELECT c.case_id,
       f.file_id,
       c.alcohol_history,
       c.cigarettes_per_day,
       c.bmi,
       CASE
           WHEN c.cigarettes_per_day IS NULL THEN 'Unknown'
           WHEN c.cigarettes_per_day > 0 THEN 'Current/Former Smoker'
           ELSE 'Non-Smoker'
       END AS smoking_status
FROM cases AS c
JOIN expression_files_info AS f
    ON f.case_id = c.case_id
ORDER BY c.case_id, f.file_id
