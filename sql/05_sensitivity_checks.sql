-- sql/05_sensitivity_checks.sql
-- Sensitivity checks for D4, Section 6.1. Run on database credit_risk_analytics.

-- Check 1: Q4 share of defaulted exposure without missing external scores
SELECT credit_income_band,
       COUNT(*) AS applications,
       SUM(CASE WHEN target = 1 THEN amt_credit ELSE 0 END) AS defaulted_exposure,
       ROUND(100.0 * SUM(CASE WHEN target = 1 THEN amt_credit ELSE 0 END)
             / SUM(SUM(CASE WHEN target = 1 THEN amt_credit ELSE 0 END)) OVER (), 2) AS share_of_loss_pct
FROM analytics.loan_application
WHERE ext_source_2 IS NOT NULL
GROUP BY credit_income_band
ORDER BY credit_income_band;

-- How many applicants have no external score?
SELECT COUNT(*) FILTER (WHERE ext_source_2 IS NULL) AS missing_ext_source_2,
       SUM(CASE WHEN ext_source_2 IS NULL AND target = 1 THEN amt_credit ELSE 0 END) AS missing_defaulted_exposure
FROM analytics.loan_application;

-- Check 2a: default rate of the employment-code group vs the rest
SELECT days_employed_anomaly,
       COUNT(*) AS applications,
       ROUND(AVG(target) * 100, 2) AS default_rate_pct
FROM analytics.loan_application
GROUP BY days_employed_anomaly;

-- Check 2b: quartile results without the employment-code group
SELECT credit_income_band,
       ROUND(AVG(target) * 100, 2) AS default_rate_pct,
       ROUND(100.0 * SUM(CASE WHEN target = 1 THEN amt_credit ELSE 0 END)
             / SUM(SUM(CASE WHEN target = 1 THEN amt_credit ELSE 0 END)) OVER (), 2) AS share_of_loss_pct
FROM analytics.loan_application
WHERE days_employed_anomaly = FALSE
GROUP BY credit_income_band
ORDER BY credit_income_band;

-- Check 2c: very-low score band without the employment-code group
SELECT ROUND(AVG(target) * 100, 2) AS very_low_default_rate_pct
FROM analytics.loan_application
WHERE days_employed_anomaly = FALSE AND ext_source_2 < 0.25;

-- Check 3: money-weighted default rate and credit share by quartile
SELECT credit_income_band,
       SUM(amt_credit) AS total_credit,
       ROUND(100.0 * SUM(amt_credit) / SUM(SUM(amt_credit)) OVER (), 1) AS share_of_credit_pct,
       ROUND(100.0 * SUM(CASE WHEN target = 1 THEN amt_credit ELSE 0 END) / SUM(amt_credit), 2) AS loss_per_100_lent
FROM analytics.loan_application
GROUP BY credit_income_band
ORDER BY credit_income_band;
