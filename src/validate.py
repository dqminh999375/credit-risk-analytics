def validate_application(df):
    print("\n=== APPLICATION VALIDATION ===")

    duplicate_ids = df["sk_id_curr"].duplicated().sum()
    print(f"Duplicate customer IDs: {duplicate_ids:,}")

    invalid_target = (~df["target"].isin([0, 1])).sum()
    print(f"Invalid TARGET values: {invalid_target:,}")

    invalid_income = (df["amt_income_total"] <= 0).sum()
    invalid_credit = (df["amt_credit"] <= 0).sum()
    print(f"Invalid income values: {invalid_income:,}")
    print(f"Invalid credit values: {invalid_credit:,}")

    negative_age = (df["age"] <= 0).sum()
    print(f"Invalid age values: {negative_age:,}")

    return {
        "rows": len(df),
        "duplicate_ids": duplicate_ids,
        "invalid_target": invalid_target,
        "invalid_income": invalid_income,
        "invalid_credit": invalid_credit,
        "negative_age": negative_age,
    }


def validate_summary(df, name):
    print(f"\n=== {name.upper()} VALIDATION ===")

    duplicate_ids = df["sk_id_curr"].duplicated().sum()
    print(f"Duplicate customer IDs: {duplicate_ids:,}")
    print(f"Rows: {len(df):,}")
    print(f"Unique customers: {df['sk_id_curr'].nunique():,}")

    return duplicate_ids == 0