-- Cleans the expression profiles and validates the FPKM values (a negative value becomes null).
SELECT file_id,
       gene_id,
       gene_name,
       gene_type,
       unstranded,
       stranded_first,
       stranded_second,
       tpm_unstranded,
       fpkm_unstranded,
       fpkm_uq_unstranded,
       CASE WHEN fpkm_unstranded < 0 THEN NULL ELSE fpkm_unstranded END AS fpkm_unstranded_validated
FROM expression_profiles_raw
WHERE file_id IS NOT NULL AND file_id <> ''
  AND gene_id IS NOT NULL AND gene_id <> ''
ORDER BY file_id, gene_id
