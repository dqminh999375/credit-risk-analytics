import pandas as pd

from config import (
    APPLICATION_FILE,
    BUREAU_FILE,
    PREVIOUS_APPLICATION_FILE,
    APPLICATION_COLUMNS,
    BUREAU_COLUMNS,
    PREVIOUS_APPLICATION_COLUMNS,
)


def extract_application():
    print("Extracting application data...")

    df = pd.read_csv(
        APPLICATION_FILE,
        usecols=APPLICATION_COLUMNS
    )

    print(f"Application rows: {len(df):,}")

    return df


def extract_bureau():
    print("Extracting bureau data...")

    df = pd.read_csv(
        BUREAU_FILE,
        usecols=BUREAU_COLUMNS
    )

    print(f"Bureau rows: {len(df):,}")

    return df


def extract_previous_application():
    print("Extracting previous application data...")

    df = pd.read_csv(
        PREVIOUS_APPLICATION_FILE,
        usecols=PREVIOUS_APPLICATION_COLUMNS
    )

    print(f"Previous application rows: {len(df):,}")

    return df


def extract_all():

    application = extract_application()
    bureau = extract_bureau()
    previous_application = extract_previous_application()

    return application, bureau, previous_application