-- 1. Row counts (Số lượng dòng của 3 bảng)
SELECT 'loan_application' AS table_name, COUNT(*) AS total_rows FROM analytics.loan_application
UNION ALL
SELECT 'bureau_summary', COUNT(*) FROM analytics.bureau_summary
UNION ALL
SELECT 'previous_application_summary', COUNT(*) FROM analytics.previous_application_summary;

-- 2. Duplicate check (Kiểm tra trùng lặp Khóa chính - Kỳ vọng: 0)
SELECT 'loan_application' AS table_name, COUNT(*) AS duplicate_ids FROM (
    SELECT sk_id_curr FROM analytics.loan_application GROUP BY sk_id_curr HAVING COUNT(*) > 1
) AS dup_app
UNION ALL
SELECT 'bureau_summary', COUNT(*) FROM (
    SELECT sk_id_curr FROM analytics.bureau_summary GROUP BY sk_id_curr HAVING COUNT(*) > 1
) AS dup_bur
UNION ALL
SELECT 'previous_application_summary', COUNT(*) FROM (
    SELECT sk_id_curr FROM analytics.previous_application_summary GROUP BY sk_id_curr HAVING COUNT(*) > 1
) AS dup_prev;

-- 3. Orphan records check (Kiểm tra mồ côi Khóa ngoại - Kỳ vọng: 0)
SELECT COUNT(*) AS orphan_bureau FROM analytics.bureau_summary b
LEFT JOIN analytics.loan_application a ON b.sk_id_curr = a.sk_id_curr WHERE a.sk_id_curr IS NULL;

SELECT COUNT(*) AS orphan_previous FROM analytics.previous_application_summary p
LEFT JOIN analytics.loan_application a ON p.sk_id_curr = a.sk_id_curr WHERE a.sk_id_curr IS NULL;