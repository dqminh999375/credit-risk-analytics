-- =====================================================
-- 02_create_tables.sql
-- Tạo 3 bảng trong schema analytics
-- Chạy trên database: credit_risk_analytics
-- Thứ tự bắt buộc: loan_application phải tạo trước
-- =====================================================


-- -----------------------------------------------------
-- Table 1: loan_application
-- One row = one loan application (SK_ID_CURR unique)
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS analytics.loan_application (
    sk_id_curr BIGINT PRIMARY KEY,

    -- Customer profile
    code_gender VARCHAR(20),
    name_income_type VARCHAR(100),
    name_education_type VARCHAR(100),
    name_family_status VARCHAR(100),
    name_housing_type VARCHAR(100),
    occupation_type VARCHAR(100),
    cnt_children INTEGER,
    cnt_fam_members NUMERIC,

    -- Loan
    name_contract_type VARCHAR(50),
    amt_income_total NUMERIC(18,2),
    amt_credit NUMERIC(18,2),
    amt_annuity NUMERIC(18,2),
    amt_goods_price NUMERIC(18,2),

    -- Derived customer metrics
    age NUMERIC(8,2),
    age_band VARCHAR(20),
    employment_years NUMERIC(8,2),
    days_employed_anomaly BOOLEAN,

    -- Risk indicators
    credit_income_ratio NUMERIC(12,4),
    credit_income_band VARCHAR(30),
    annuity_income_ratio NUMERIC(12,4),

    -- External scores
    ext_source_1 NUMERIC(10,6),
    ext_source_2 NUMERIC(10,6),
    ext_source_3 NUMERIC(10,6),

    -- Credit enquiries
    amt_req_credit_bureau_year NUMERIC(10,2),

    -- Target
    target SMALLINT
);


-- -----------------------------------------------------
-- Table 2: bureau_summary
-- One row = one customer (aggregated from bureau)
-- FK: sk_id_curr references loan_application
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS analytics.bureau_summary (
    sk_id_curr BIGINT PRIMARY KEY,

    previous_credit_count INTEGER,
    active_credit_count INTEGER,
    closed_credit_count INTEGER,
    overdue_credit_count INTEGER,
    overdue_credit_rate NUMERIC(12,4),
    total_credit_sum NUMERIC(18,2),
    avg_credit_amount NUMERIC(18,2),
    max_overdue_amount NUMERIC(18,2),
    total_debt NUMERIC(18,2),

    CONSTRAINT fk_bureau_customer
        FOREIGN KEY (sk_id_curr)
        REFERENCES analytics.loan_application(sk_id_curr)
);


-- -----------------------------------------------------
-- Table 3: previous_application_summary
-- One row = one customer (aggregated from previous_application)
-- FK: sk_id_curr references loan_application
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS analytics.previous_application_summary (
    sk_id_curr BIGINT PRIMARY KEY,

    previous_application_count INTEGER,
    approved_application_count INTEGER,
    refused_application_count INTEGER,
    previous_refusal_rate NUMERIC(12,4),
    avg_previous_credit NUMERIC(18,2),
    avg_previous_annuity NUMERIC(18,2),

    CONSTRAINT fk_previous_customer
        FOREIGN KEY (sk_id_curr)
        REFERENCES analytics.loan_application(sk_id_curr)
);