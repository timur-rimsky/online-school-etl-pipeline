from pathlib import Path

import numpy as np
import pandas as pd


def generate_payments() -> pd.DataFrame:
    """
    Generate synthetic payments data for an online school ETL project.
    Payments are generated only for leads with the 'converted' status.
    Each row represents one payment attempt for a course.
    """
    np.random.seed(42)

    project_root = Path(__file__).resolve().parents[1]

    leads_path = project_root / "data" / "raw" / "leads.csv"
    courses_path = project_root / "data" / "raw" / "courses.csv"

    leads = pd.read_csv(leads_path)
    courses = pd.read_csv(courses_path)

    converted_leads = leads[leads["lead_status"] == "converted"].copy()

    n_payments = len(converted_leads)

    payment_ids = np.arange(1, n_payments + 1)

    converted_leads["lead_date"] = pd.to_datetime(converted_leads["lead_date"])

    payment_dates = converted_leads["lead_date"] + pd.to_timedelta(
        np.random.randint(0, 8, size=n_payments),
        unit="D"
    )

    course_prices = courses.set_index("course_id")["course_price"]

    amounts = converted_leads["course_id"].map(course_prices)

    payment_statuses = np.random.choice(
        ["paid", "refunded"],
        size=n_payments,
        p=[0.92, 0.08]
    )

    payments = pd.DataFrame({
        "payment_id": payment_ids,
        "user_id": converted_leads["user_id"].values,
        "course_id": converted_leads["course_id"].values,
        "payment_date": payment_dates.values,
        "amount": amounts.values,
        "payment_status": payment_statuses
    })

    return payments


def save_payments(payments: pd.DataFrame) -> None:
    """
    Save payments dataframe to data/raw/payments.csv.
    """
    project_root = Path(__file__).resolve().parents[1]
    output_path = project_root / "data" / "raw" / "payments.csv"

    output_path.parent.mkdir(parents=True, exist_ok=True)

    payments.to_csv(output_path, index=False)

    print(f"payments.csv saved to: {output_path}")
    print(f"Rows: {len(payments)}")
    print(f"Columns: {payments.shape[1]}")


if __name__ == "__main__":
    payments_df = generate_payments()
    save_payments(payments_df)