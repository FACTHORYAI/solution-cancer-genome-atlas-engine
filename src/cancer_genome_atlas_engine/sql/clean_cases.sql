-- Cleans the clinical cases, keeping the rows that carry a case identifier.
SELECT case_id,
       gender,
       race,
       ethnicity,
       year_of_birth,
       year_of_death,
       vital_status,
       primary_diagnosis,
       tissue_or_organ_of_origin,
       tumor_grade,
       classification_of_tumor,
       treatments,
       alcohol_history,
       cigarettes_per_day,
       bmi
FROM cases_raw
WHERE case_id IS NOT NULL AND case_id <> ''
ORDER BY case_id
