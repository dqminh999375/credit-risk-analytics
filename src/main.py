from pathlib import Path

from config import (
    PROCESSED_DIR,
    APPLICATION_OUTPUT,
    BUREAU_OUTPUT,
    PREVIOUS_APPLICATION_OUTPUT
)

from extract import extract_all

from transform import (
    transform_application,
    transform_bureau,
    transform_previous_application
)

from validate import (
    validate_application,
    validate_summary
)


def main():

    print("=" * 60)
    print("CREDIT RISK ETL PIPELINE")
    print("=" * 60)


    # --------------------------------------------------
    # 1. Create processed directory
    # --------------------------------------------------

    PROCESSED_DIR.mkdir(
        parents=True,
        exist_ok=True
    )


    # --------------------------------------------------
    # 2. EXTRACT
    # --------------------------------------------------

    application, bureau, previous_application = (
        extract_all()
    )


    # --------------------------------------------------
    # 3. TRANSFORM
    # --------------------------------------------------

    print("\nTransforming application...")
    application_clean = transform_application(
        application
    )

    print("Transforming bureau...")
    bureau_summary = transform_bureau(
        bureau
    )

    print("Transforming previous applications...")
    previous_application_summary = (
        transform_previous_application(
            previous_application
        )
    )


    # --------------------------------------------------
    # 4. VALIDATE
    # --------------------------------------------------

    validate_application(
        application_clean
    )

    validate_summary(
        bureau_summary,
        "Bureau Summary"
    )

    validate_summary(
        previous_application_summary,
        "Previous Application Summary"
    )


    # --------------------------------------------------
    # 5. SAVE
    # --------------------------------------------------

    print("\nSaving processed datasets...")

    application_clean.to_csv(
        APPLICATION_OUTPUT,
        index=False
    )

    bureau_summary.to_csv(
        BUREAU_OUTPUT,
        index=False
    )

    previous_application_summary.to_csv(
        PREVIOUS_APPLICATION_OUTPUT,
        index=False
    )


    # --------------------------------------------------
    # 6. Final report
    # --------------------------------------------------

    print("\n" + "=" * 60)
    print("ETL COMPLETED")
    print("=" * 60)

    print(
        f"Application: "
        f"{application_clean.shape}"
    )

    print(
        f"Bureau summary: "
        f"{bureau_summary.shape}"
    )

    print(
        f"Previous application summary: "
        f"{previous_application_summary.shape}"
    )

    print(
        f"\nProcessed files saved to:"
        f"\n{PROCESSED_DIR}"
    )


if __name__ == "__main__":
    main()