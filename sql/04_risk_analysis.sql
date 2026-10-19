-- =====================================================
-- 04_risk_analysis.sql
-- SQL risk analysis cho D4 Results section
-- Chạy trên database: credit_risk_analytics
-- =====================================================


-- =====================================================
-- QUERY 1: Overall portfolio KPI
-- Dùng cho D4 Section 5.2
-- =====================================================
SELECT
    COUNT(*) AS total_applications,
    SUM(amt_credit) AS total_credit_exposure,
    SUM(CASE WHEN target = 1 THEN amt_credit ELSE 0 END) AS defaulted_exposure,
    ROUND(AVG(target) * 100, 2) AS observed_default_rate_pct
FROM analytics.loan_application;


-- =====================================================
-- QUERY 2: Default rate by contract type
-- Dùng cho D4 Section 5.3
-- =====================================================
SELECT
    name_contract_type,

    COUNT(*) AS applications,

    ROUND(AVG(target) * 100, 2) AS observed_default_rate_pct,

    SUM(amt_credit) AS total_credit,

    SUM(CASE
        WHEN target = 1 THEN amt_credit
        ELSE 0
    END) AS defaulted_exposure

FROM analytics.loan_application

GROUP BY name_contract_type

ORDER BY observed_default_rate_pct DESC;


-- =====================================================
-- QUERY 3: Default rate by age band
-- Dùng cho D4 Section 5.3
-- =====================================================
SELECT
    age_band,

    COUNT(*) AS applications,

    ROUND(AVG(target) * 100, 2) AS observed_default_rate_pct,

    SUM(amt_credit) AS total_credit,

    SUM(CASE
        WHEN target = 1 THEN amt_credit
        ELSE 0
    END) AS defaulted_exposure

FROM analytics.loan_application

GROUP BY age_band

ORDER BY age_band;


-- =====================================================
-- QUERY 4: Default rate by credit-to-income band
-- Dùng cho D4 Section 5.3 (query quan trọng nhất)
-- =====================================================
SELECT
    credit_income_band,

    COUNT(*) AS applications,

    ROUND(AVG(target) * 100, 2) AS observed_default_rate_pct,

    AVG(credit_income_ratio) AS avg_credit_income_ratio,

    SUM(amt_credit) AS total_credit,

    SUM(CASE
        WHEN target = 1 THEN amt_credit
        ELSE 0
    END) AS defaulted_exposure

FROM analytics.loan_application

GROUP BY credit_income_band

ORDER BY credit_income_band;


-- =====================================================
-- QUERY 5: Default rate by external score band (EXT_SOURCE_2)
-- Dùng cho D4 Section 5.3
-- =====================================================
SELECT
    CASE
        WHEN ext_source_2 < 0.25 THEN '1. Very Low'
        WHEN ext_source_2 < 0.50 THEN '2. Low'
        WHEN ext_source_2 < 0.75 THEN '3. Medium'
        ELSE '4. High'
    END AS external_score_band,

    COUNT(*) AS applications,

    ROUND(AVG(target) * 100, 2) AS observed_default_rate_pct,

    SUM(amt_credit) AS total_credit,

    SUM(CASE
        WHEN target = 1 THEN amt_credit
        ELSE 0
    END) AS defaulted_exposure

FROM analytics.loan_application

WHERE ext_source_2 IS NOT NULL

GROUP BY 1

ORDER BY 1;


-- =====================================================
-- QUERY 6: Default rate by previous overdue history
-- Dùng cho D4 Section 5.3 (credit history × current risk)
-- =====================================================
SELECT
    CASE
        WHEN b.overdue_credit_count IS NULL
            THEN '0. No bureau record'

        WHEN b.overdue_credit_count = 0
            THEN '1. No previous overdue'

        WHEN b.overdue_credit_count BETWEEN 1 AND 2
            THEN '2. 1-2 previous overdue'

        ELSE '3. 3+ previous overdue'
    END AS overdue_history_band,

    COUNT(*) AS applications,

    ROUND(AVG(a.target) * 100, 2) AS observed_default_rate_pct,

    SUM(a.amt_credit) AS total_credit,

    SUM(CASE
        WHEN a.target = 1 THEN a.amt_credit
        ELSE 0
    END) AS defaulted_exposure

FROM analytics.loan_application a

LEFT JOIN analytics.bureau_summary b
    ON a.sk_id_curr = b.sk_id_curr

GROUP BY 1

ORDER BY 1;


-- =====================================================
-- QUERY 7: Default rate by previous application refusal
-- Dùng cho D4 Section 5.3
-- =====================================================
SELECT
    CASE
        WHEN p.previous_refusal_rate IS NULL
            THEN '0. No previous application'

        WHEN p.previous_refusal_rate = 0
            THEN '1. 0% refused'

        WHEN p.previous_refusal_rate < 0.5
            THEN '2. 1-49% refused'

        ELSE '3. 50%+ refused'
    END AS refusal_history_band,

    COUNT(*) AS applications,

    ROUND(AVG(a.target) * 100, 2) AS observed_default_rate_pct,

    SUM(a.amt_credit) AS total_credit,

    SUM(CASE
        WHEN a.target = 1 THEN a.amt_credit
        ELSE 0
    END) AS defaulted_exposure

FROM analytics.loan_application a

LEFT JOIN analytics.previous_application_summary p
    ON a.sk_id_curr = p.sk_id_curr

GROUP BY 1

ORDER BY 1;


-- =====================================================
-- QUERY 8: Risk × Exposure — quan trọng nhất cho D4 Section 5.4
-- Sort by defaulted_exposure (không phải rate)
-- =====================================================
SELECT
    credit_income_band,
    COUNT(*) AS applications,
    ROUND(AVG(target) * 100, 2) AS observed_default_rate_pct,
    SUM(amt_credit) AS total_credit,
    SUM(CASE WHEN target = 1 THEN amt_credit ELSE 0 END) AS defaulted_exposure
FROM analytics.loan_application
GROUP BY credit_income_band
ORDER BY defaulted_exposure DESC;