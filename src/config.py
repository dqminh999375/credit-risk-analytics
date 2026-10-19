from pathlib import Path


# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Data directories
RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"


# Raw files
APPLICATION_FILE = RAW_DIR / "application_train.csv"
BUREAU_FILE = RAW_DIR / "bureau.csv"
PREVIOUS_APPLICATION_FILE = RAW_DIR / "previous_application.csv"


# Processed files
APPLICATION_OUTPUT = PROCESSED_DIR / "application_clean.csv"
BUREAU_OUTPUT = PROCESSED_DIR / "bureau_summary.csv"
PREVIOUS_APPLICATION_OUTPUT = (
    PROCESSED_DIR / "previous_application_summary.csv"
)


# Application columns
APPLICATION_COLUMNS = [
    "SK_ID_CURR",
    "CODE_GENDER",
    "AMT_INCOME_TOTAL",
    "NAME_INCOME_TYPE",
    "NAME_EDUCATION_TYPE",
    "NAME_FAMILY_STATUS",
    "NAME_HOUSING_TYPE",
    "CNT_CHILDREN",
    "CNT_FAM_MEMBERS",
    "NAME_CONTRACT_TYPE",
    "AMT_CREDIT",
    "AMT_ANNUITY",
    "AMT_GOODS_PRICE",
    "DAYS_BIRTH",
    "DAYS_EMPLOYED",
    "OCCUPATION_TYPE",
    "EXT_SOURCE_1",
    "EXT_SOURCE_2",
    "EXT_SOURCE_3",
    "AMT_REQ_CREDIT_BUREAU_YEAR",
    "TARGET",
]


# Bureau columns
BUREAU_COLUMNS = [
    "SK_ID_CURR",
    "SK_ID_BUREAU",
    "CREDIT_ACTIVE",
    "DAYS_CREDIT",
    "CREDIT_DAY_OVERDUE",
    "AMT_CREDIT_MAX_OVERDUE",
    "AMT_CREDIT_SUM",
    "AMT_CREDIT_SUM_DEBT",
    "AMT_CREDIT_SUM_OVERDUE",
]


# Previous application columns
PREVIOUS_APPLICATION_COLUMNS = [
    "SK_ID_CURR",
    "SK_ID_PREV",
    "NAME_CONTRACT_STATUS",
    "AMT_CREDIT",
    "AMT_ANNUITY",
]