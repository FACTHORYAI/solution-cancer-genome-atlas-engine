-- Silver: patient diagnoses with a treatment flag, one row per sample file.
SELECT c.case_id,
       f.file_id,
       c.classification_of_tumor,
       c.primary_diagnosis,
       c.tissue_or_organ_of_origin,
       c.tumor_grade,
       (c.treatments IS NOT NULL AND c.treatments <> '') AS has_treatment
FROM cases AS c
JOIN expression_files_info AS f
    ON f.case_id = c.case_id
ORDER BY c.case_id, f.file_id
