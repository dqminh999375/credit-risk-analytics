# application transformation -> bureau aggregation -> previous application aggregation
import numpy as np
import pandas as pd


# ==================================================
# APPLICATION TRANSFORM
# ==================================================
def transform_application(df):

    df = df.copy()

    # Chuẩn hóa tên cột về chữ thường
    df.columns = df.columns.str.lower()

    # --------------------------------------------------
    # 1. Remove duplicate customer/application IDs
    # --------------------------------------------------

    df = df.drop_duplicates(subset="sk_id_curr")

    # --------------------------------------------------
    # 2. Handle DAYS_EMPLOYED anomaly
    # --------------------------------------------------

    df["days_employed_anomaly"] = (
        df["days_employed"] == 365243
    )

    df["days_employed_clean"] = df["days_employed"].replace(
        365243,
        np.nan
    )
    # The raw employment-day field contained an extreme coded value of 365,243.
    # Instead of treating it as a valid employment duration, I preserved an
    # anomaly flag and converted the value to missing before deriving
    # employment years.

    # --------------------------------------------------
    # 3. Age
    # --------------------------------------------------

    df["age"] = (
        -df["days_birth"] / 365.25
    )

    # --------------------------------------------------
    # 4. Employment years
    # --------------------------------------------------

    df["employment_years"] = (
        -df["days_employed_clean"] / 365.25
    )

    # --------------------------------------------------
    # 5. Credit-to-income ratio
    # --------------------------------------------------

    df["credit_income_ratio"] = (
        df["amt_credit"] /
        df["amt_income_total"]
    )

    # --------------------------------------------------
    # 6. Annuity-to-income ratio
    # --------------------------------------------------

    df["annuity_income_ratio"] = (
        df["amt_annuity"] /
        df["amt_income_total"]
    )

    # --------------------------------------------------
    # 7. Risk segmentation bands
    # --------------------------------------------------

    df["age_band"] = pd.cut(
        df["age"],
        bins=[0, 25, 35, 45, 55, np.inf],
        labels=[
            "<25",
            "25-34",
            "35-44",
            "45-54",
            "55+"
        ],
        right=False
    )

    # --------------------------------------------------
    # 8. Credit-to-income quartile
    # --------------------------------------------------

    df["credit_income_band"] = pd.qcut(
        df["credit_income_ratio"],
        q=4,
        labels=[
            "Q1 - Lowest",
            "Q2",
            "Q3",
            "Q4 - Highest"
        ],
        duplicates="drop"
    )

    # --------------------------------------------------
    # 9. Final columns
    # --------------------------------------------------

    final_columns = [
        "sk_id_curr",

        # Customer profile
        "code_gender",
        "name_income_type",
        "name_education_type",
        "name_family_status",
        "name_housing_type",
        "occupation_type",
        "cnt_children",
        "cnt_fam_members",

        # Loan
        "name_contract_type",
        "amt_income_total",
        "amt_credit",
        "amt_annuity",
        "amt_goods_price",

        # Derived customer metrics
        "age",
        "age_band",
        "employment_years",
        "days_employed_anomaly",

        # Risk indicators
        "credit_income_ratio",
        "credit_income_band",
        "annuity_income_ratio",

        # External scores
        "ext_source_1",
        "ext_source_2",
        "ext_source_3",

        # Credit enquiries
        "amt_req_credit_bureau_year",

        # Target
        "target"
    ]

    df = df[final_columns]

    return df


# ==================================================
# BUREAU TRANSFORM
# ==================================================
def transform_bureau(df):

    df = df.copy()

    # Chuẩn hóa tên cột về chữ thường
    df.columns = df.columns.str.lower()

    df["overdue_flag"] = (
        (df["credit_day_overdue"] > 0) |
        (df["amt_credit_sum_overdue"] > 0)
    )

    summary = (
        df.groupby("sk_id_curr")
        .agg(
            previous_credit_count=(
                "sk_id_bureau",
                "nunique"
            ),

            active_credit_count=(
                "credit_active",
                lambda x: (x == "Active").sum()
            ),

            closed_credit_count=(
                "credit_active",
                lambda x: (x == "Closed").sum()
            ),

            overdue_credit_count=(
                "overdue_flag",
                "sum"
            ),

            total_credit_sum=(
                "amt_credit_sum",
                "sum"
            ),

            avg_credit_amount=(
                "amt_credit_sum",
                "mean"
            ),

            max_overdue_amount=(
                "amt_credit_sum_overdue",
                "max"
            ),

            total_debt=(
                "amt_credit_sum_debt",
                "sum"
            )
        )
        .reset_index()
    )

    summary["overdue_credit_rate"] = (
        summary["overdue_credit_count"] /
        summary["previous_credit_count"]
    )

    return summary


# ==================================================
# PREVIOUS APPLICATION TRANSFORM
# ==================================================
def transform_previous_application(df):

    df = df.copy()

    # Chuẩn hóa tên cột về chữ thường
    df.columns = df.columns.str.lower()

    summary = (
        df.groupby("sk_id_curr")
        .agg(
            previous_application_count=(
                "sk_id_prev",
                "nunique"
            ),

            approved_application_count=(
                "name_contract_status",
                lambda x: (x == "Approved").sum()
            ),

            refused_application_count=(
                "name_contract_status",
                lambda x: (x == "Refused").sum()
            ),

            avg_previous_credit=(
                "amt_credit",
                "mean"
            ),

            avg_previous_annuity=(
                "amt_annuity",
                "mean"
            )
        )
        .reset_index()
    )

    summary["previous_refusal_rate"] = (
        summary["refused_application_count"] /
        summary["previous_application_count"]
    )

    return summary