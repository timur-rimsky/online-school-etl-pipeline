from extract import extract_data
from transform import transform_data
from load import load_data


def print_step(message: str) -> None:
    print("=" * 50)
    print(message)


def run_pipeline() -> None:
    print_step("Starting ETL pipeline...")

    raw_data = extract_data()
    print_step("Extract completed.")

    cleaned_data = transform_data(raw_data)
    print_step("Transform completed.")

    load_data(cleaned_data)
    print_step("Load completed.")

    print_step("ETL pipeline completed successfully.")


if __name__ == "__main__":
    run_pipeline()