-- Cleans the file metadata, keeping the rows that carry both identifiers.
SELECT file_id,
       case_id,
       project_id,
       file_size,
       data_format,
       sample_type
FROM expression_files_info_raw
WHERE file_id IS NOT NULL AND file_id <> ''
  AND case_id IS NOT NULL AND case_id <> ''
ORDER BY file_id
