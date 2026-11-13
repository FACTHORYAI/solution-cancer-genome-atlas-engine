-- One row per sample with its reduced coordinates and its diagnosis, for clustering.
SELECT c.file_id,
       c.pc1,
       c.pc2,
       c.pc3,
       c.tsne_1,
       c.tsne_2,
       d.tissue_or_organ_of_origin,
       d.primary_diagnosis,
       d.tumor_grade
FROM expression_coordinates AS c
LEFT JOIN cases_diagnoses AS d
    ON d.file_id = c.file_id
ORDER BY c.file_id
