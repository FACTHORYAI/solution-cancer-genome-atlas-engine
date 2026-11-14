-- Joins the cases to their sample files: demographics with a vital-status flag, one row per sample file.
SELECT c.case_id,
       f.file_id,
       c.gender,
       c.race,
       c.ethnicity,
       c.year_of_birth,
       c.year_of_death,
       c.year_of_death IS NOT NULL AS is_deceased
FROM cases AS c
JOIN expression_files_info AS f
    ON f.case_id = c.case_id
ORDER BY c.case_id, f.file_id
