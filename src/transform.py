import pandas as pd

from extract import extract_data


# =========================
# Constants
# =========================

REQUIRED_TABLES = ["users", "courses", "leads", "payments", "lessons"]

LEAD_STATUSES = ["new", "contacted", "qualified", "lost", "converted"]
PAYMENT_STATUSES = ["paid", "refunded"]
LESSON_TYPES = ["webinar", "practice", "homework_review", "consultation"]
ATTENDANCE_STATUSES = ["attended", "missed", "cancelled"]


# =========================
# Validation helpers
# =========================

def validate_required_tables(data: dict[str, pd.DataFrame]) -> None:
    """
    Check that all required tables are present in the input dictionary.
    """
    missing_tables = [
        table_name
        for table_name in REQUIRED_TABLES
        if table_name not in data
    ]

    if missing_tables:
        raise KeyError(f"Missing required tables: {missing_tables}")


def validate_required_columns(
    table: pd.DataFrame,
    table_name: str,
    columns: list[str]
) -> None:
    """
    Check that all required columns are present in a DataFrame.
    """
    missing_columns = [
        column
        for column in columns
        if column not in table.columns
    ]

    if missing_columns:
        raise KeyError(
            f"Missing columns in '{table_name}': {missing_columns}"
        )


# =========================
# Transformation helpers
# =========================

def drop_required_rows(
    table: pd.DataFrame,
    columns: list[str]
) -> pd.DataFrame:
    """
    Drop rows with missing values in required columns.
    """
    return table.dropna(subset=columns).copy()


def drop_duplicate_key(
    table: pd.DataFrame,
    key: str
) -> pd.DataFrame:
    """
    Drop duplicate rows by a primary key column.
    """
    return table.drop_duplicates(subset=key).copy()


def convert_columns_to_numeric(
    table: pd.DataFrame,
    columns: list[str]
) -> pd.DataFrame:
    """
    Convert selected columns to numeric values.
    Invalid values are converted to NaN and then removed.
    """
    table = table.copy()

    for column in columns:
        table[column] = pd.to_numeric(table[column], errors="coerce")

    return table.dropna(subset=columns).copy()


def convert_columns_to_int(
    table: pd.DataFrame,
    columns: list[str]
) -> pd.DataFrame:
    """
    Convert selected columns to integer values.
    Invalid values are converted to NaN and then removed.
    """
    table = convert_columns_to_numeric(table, columns)

    for column in columns:
        table = table[table[column] % 1 == 0].copy()
        table[column] = table[column].astype("int")

    return table


def convert_columns_to_datetime(
    table: pd.DataFrame,
    columns: list[str]
) -> pd.DataFrame:
    """
    Convert selected columns to datetime.
    Invalid dates are converted to NaT and then removed.
    """
    table = table.copy()

    for column in columns:
        table[column] = pd.to_datetime(table[column], errors="coerce")

    return table.dropna(subset=columns).copy()


def normalize_text_columns(
    table: pd.DataFrame,
    columns: list[str]
) -> pd.DataFrame:
    """
    Strip spaces and convert selected text columns to lowercase.
    """
    table = table.copy()

    for column in columns:
        table[column] = table[column].str.strip().str.lower()

    return table


def filter_allowed_values(
    table: pd.DataFrame,
    column: str,
    allowed_values: list[str | int]
) -> pd.DataFrame:
    """
    Keep only rows where the column contains allowed values.
    """
    return table[table[column].isin(allowed_values)].copy()


def filter_positive_values(
    table: pd.DataFrame,
    columns: list[str]
) -> pd.DataFrame:
    """
    Keep only rows where selected numeric columns are greater than zero.
    """
    table = table.copy()

    for column in columns:
        table = table[table[column] > 0].copy()

    return table


def filter_range(
    table: pd.DataFrame,
    column: str,
    min_value: int | float,
    max_value: int | float
) -> pd.DataFrame:
    """
    Keep only rows where the column value is within the specified range.
    """
    return table[
        (table[column] >= min_value) &
        (table[column] <= max_value)
    ].copy()


def finalize_table(table: pd.DataFrame) -> pd.DataFrame:
    """
    Reset DataFrame index after cleaning.
    """
    return table.reset_index(drop=True)


# =========================
# Table-specific cleaning
# =========================

def clean_users(users: pd.DataFrame) -> pd.DataFrame:
    """
    Clean users table.
    """
    required_columns = [
        "user_id",
        "registration_date",
        "country",
        "city",
        "age",
        "traffic_source",
        "device",
        "is_active"
    ]

    validate_required_columns(users, "users", required_columns)

    table = users.copy()

    table = drop_required_rows(
        table,
        ["user_id", "registration_date", "age", "is_active"]
    )

    table = drop_duplicate_key(table, "user_id")

    table = convert_columns_to_int(
        table,
        ["user_id", "age", "is_active"]
    )

    table = convert_columns_to_datetime(
        table,
        ["registration_date"]
    )

    table = filter_range(
        table,
        column="age",
        min_value=18,
        max_value=80
    )

    table = filter_allowed_values(
        table,
        column="is_active",
        allowed_values=[0, 1]
    )

    return finalize_table(table)


def clean_courses(courses: pd.DataFrame) -> pd.DataFrame:
    """
    Clean courses table.
    """
    required_columns = [
        "course_id",
        "course_name",
        "category",
        "course_price",
        "duration_weeks"
    ]

    validate_required_columns(courses, "courses", required_columns)

    table = courses.copy()

    table = drop_required_rows(
        table,
        ["course_id", "course_name", "category", "course_price", "duration_weeks"]
    )

    table = drop_duplicate_key(table, "course_id")

    table = convert_columns_to_int(
        table,
        ["course_id", "duration_weeks"]
    )

    table = convert_columns_to_numeric(
        table,
        ["course_price"]
    )

    table = filter_positive_values(
        table,
        ["course_price", "duration_weeks"]
    )

    return finalize_table(table)


def clean_leads(leads: pd.DataFrame) -> pd.DataFrame:
    """
    Clean leads table.
    """
    required_columns = [
        "lead_id",
        "user_id",
        "course_id",
        "lead_date",
        "lead_status"
    ]

    validate_required_columns(leads, "leads", required_columns)

    table = leads.copy()

    table = drop_required_rows(
        table,
        ["lead_id", "user_id", "course_id", "lead_date", "lead_status"]
    )

    table = drop_duplicate_key(table, "lead_id")

    table = convert_columns_to_int(
        table,
        ["lead_id", "user_id", "course_id"]
    )

    table = convert_columns_to_datetime(
        table,
        ["lead_date"]
    )

    table = normalize_text_columns(
        table,
        ["lead_status"]
    )

    table = filter_allowed_values(
        table,
        column="lead_status",
        allowed_values=LEAD_STATUSES
    )

    return finalize_table(table)


def clean_payments(payments: pd.DataFrame) -> pd.DataFrame:
    """
    Clean payments table.
    """
    required_columns = [
        "payment_id",
        "user_id",
        "course_id",
        "payment_date",
        "amount",
        "payment_status"
    ]

    validate_required_columns(payments, "payments", required_columns)

    table = payments.copy()

    table = drop_required_rows(
        table,
        ["payment_id", "user_id", "course_id", "payment_date", "amount", "payment_status"]
    )

    table = drop_duplicate_key(table, "payment_id")

    table = convert_columns_to_int(
        table,
        ["payment_id", "user_id", "course_id"]
    )

    table = convert_columns_to_datetime(
        table,
        ["payment_date"]
    )

    table = convert_columns_to_numeric(
        table,
        ["amount"]
    )

    table = filter_positive_values(
        table,
        ["amount"]
    )

    table = normalize_text_columns(
        table,
        ["payment_status"]
    )

    table = filter_allowed_values(
        table,
        column="payment_status",
        allowed_values=PAYMENT_STATUSES
    )

    return finalize_table(table)


def clean_lessons(lessons: pd.DataFrame) -> pd.DataFrame:
    """
    Clean lessons table.
    """
    required_columns = [
        "lesson_id",
        "user_id",
        "course_id",
        "lesson_date",
        "lesson_type",
        "attendance_status"
    ]

    validate_required_columns(lessons, "lessons", required_columns)

    table = lessons.copy()

    table = drop_required_rows(
        table,
        ["lesson_id", "user_id", "course_id", "lesson_date", "lesson_type", "attendance_status"]
    )

    table = drop_duplicate_key(table, "lesson_id")

    table = convert_columns_to_int(
        table,
        ["lesson_id", "user_id", "course_id"]
    )

    table = convert_columns_to_datetime(
        table,
        ["lesson_date"]
    )

    table = normalize_text_columns(
        table,
        ["lesson_type", "attendance_status"]
    )

    table = filter_allowed_values(
        table,
        column="lesson_type",
        allowed_values=LESSON_TYPES
    )

    table = filter_allowed_values(
        table,
        column="attendance_status",
        allowed_values=ATTENDANCE_STATUSES
    )

    return finalize_table(table)


# =========================
# Main transform function
# =========================

def transform_data(data: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    """
    Apply all table-specific transformations and return cleaned data.
    """
    validate_required_tables(data)

    return {
        "users": clean_users(data["users"]),
        "courses": clean_courses(data["courses"]),
        "leads": clean_leads(data["leads"]),
        "payments": clean_payments(data["payments"]),
        "lessons": clean_lessons(data["lessons"]),
    }


# =========================
# Script entry point
# =========================

if __name__ == "__main__":
    raw_data = extract_data()
    cleaned_data = transform_data(raw_data)

    for table_name, dataframe in cleaned_data.items():
        print(f"{table_name}: {dataframe.shape}")