import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text


# ============================================================
# 1. PROJECT PATH
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]
ENV_FILE = PROJECT_ROOT / ".env"
load_dotenv(ENV_FILE)


# ============================================================
# 2. DATABASE CONFIGURATION
# ============================================================

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

required_variables = {
    "DB_HOST": DB_HOST,
    "DB_PORT": DB_PORT,
    "DB_NAME": DB_NAME,
    "DB_USER": DB_USER,
    "DB_PASSWORD": DB_PASSWORD,
}

missing = [k for k, v in required_variables.items() if not v]
if missing:
    raise ValueError(f"Missing environment variables: {missing}")


DATABASE_URL = (
    f"postgresql+psycopg2://"
    f"{DB_USER}:{DB_PASSWORD}@"
    f"{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(DATABASE_URL)


# ============================================================
# 3. PATHS TO PROCESSED CSV
# ============================================================

PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

APPLICATION_FILE = PROCESSED_DIR / "application_clean.csv"
BUREAU_FILE = PROCESSED_DIR / "bureau_summary.csv"
PREVIOUS_APPLICATION_FILE = PROCESSED_DIR / "previous_application_summary.csv"


# ============================================================
# 4. LOAD FUNCTIONS
# ============================================================

def load_application():
    print("\nLoading application table...")

    df = pd.read_csv(APPLICATION_FILE)
    df.columns = df.columns.str.lower()
    print(f"  Read {len(df):,} rows from {APPLICATION_FILE.name}")
    print(f"  Columns: {df.columns.tolist()}")

    df.to_sql(
        "loan_application",
        engine,
        schema="analytics",
        if_exists="append",
        index=False,
        chunksize=1000,
        method=None,
    )
    print(f"  Loaded {len(df):,} rows into analytics.loan_application")


def load_bureau():
    print("\nLoading bureau summary...")

    df = pd.read_csv(BUREAU_FILE)
    df.columns = df.columns.str.lower()
    print(f"  Read {len(df):,} rows from {BUREAU_FILE.name}")

    # --- BẮT ĐẦU PHẦN SỬA LỖI FK ---
    # Đọc danh sách khách hợp lệ từ application
    application_df = pd.read_csv(APPLICATION_FILE)
    application_df.columns = application_df.columns.str.lower()
    valid_customers = set(application_df["sk_id_curr"].unique())

    # Lọc bỏ các khách không có trong application
    before = len(df)
    df = df[df["sk_id_curr"].isin(valid_customers)]
    after = len(df)

    print(f"  Filtered: {before - after:,} customers not in loan_application")
    print(f"  Keeping: {after:,} customers")
    # --- KẾT THÚC PHẦN SỬA LỖI FK ---

    df.to_sql(
        "bureau_summary",
        engine,
        schema="analytics",
        if_exists="append",
        index=False,
        chunksize=1000,
        method=None,
    )
    print(f"  Loaded {len(df):,} rows into analytics.bureau_summary")


def load_previous_application():
    print("\nLoading previous application summary...")

    df = pd.read_csv(PREVIOUS_APPLICATION_FILE)
    df.columns = df.columns.str.lower()
    print(f"  Read {len(df):,} rows from {PREVIOUS_APPLICATION_FILE.name}")

    # --- BẮT ĐẦU PHẦN SỬA LỖI FK ---
    # Đọc danh sách khách hợp lệ từ application
    application_df = pd.read_csv(APPLICATION_FILE)
    application_df.columns = application_df.columns.str.lower()
    valid_customers = set(application_df["sk_id_curr"].unique())

    # Lọc bỏ các khách không có trong application
    before = len(df)
    df = df[df["sk_id_curr"].isin(valid_customers)]
    after = len(df)

    print(f"  Filtered: {before - after:,} customers not in loan_application")
    print(f"  Keeping: {after:,} customers")
    # --- KẾT THÚC PHẦN SỬA LỖI FK ---

    df.to_sql(
        "previous_application_summary",
        engine,
        schema="analytics",
        if_exists="append",
        index=False,
        chunksize=1000,
        method=None,
    )
    print(
        f"  Loaded {len(df):,} rows into "
        f"analytics.previous_application_summary"
    )


# ============================================================
# 5. MAIN
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("LOADING PROCESSED DATA INTO POSTGRESQL")
    print("=" * 60)

    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print("PostgreSQL connection successful:", result.scalar())

    # Bắt buộc đúng thứ tự: cha trước, con sau
    load_application()
    load_bureau()
    load_previous_application()

    print("\n" + "=" * 60)
    print("DATABASE LOADING COMPLETED")
    print("=" * 60)