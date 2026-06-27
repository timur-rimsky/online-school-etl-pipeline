from pathlib import Path

import numpy as np
import pandas as pd


def generate_leads(n_leads: int = 3500) -> pd.DataFrame:
    """
    Generate synthetic leads data for an online school ETL project.
    Each row represents one course application submitted by a user.
    """
    np.random.seed(42)

    project_root = Path(__file__).resolve().parents[1]

    users_path = project_root / "data" / "raw" / "users.csv"
    courses_path = project_root / "data" / "raw" / "courses.csv"

    users = pd.read_csv(users_path)
    courses = pd.read_csv(courses_path)

    lead_ids = np.arange(1, n_leads + 1)

    user_ids = np.random.choice(
        users["user_id"],
        size=n_leads,
        replace=False
    )

    course_ids = np.random.choice(
        courses["course_id"],
        size=n_leads,
        p=[0.22, 0.20, 0.18, 0.16, 0.12, 0.12]
    )

    lead_dates = pd.to_datetime(
        np.random.choice(
            pd.date_range(start="2026-01-05", end="2026-04-15"),
            size=n_leads
        )
    )

    lead_statuses = np.random.choice(
        ["new", "contacted", "qualified", "lost", "converted"],
        size=n_leads,
        p=[0.18, 0.22, 0.20, 0.25, 0.15]
    )

    leads = pd.DataFrame({
        "lead_id": lead_ids,
        "user_id": user_ids,
        "course_id": course_ids,
        "lead_date": lead_dates,
        "lead_status": lead_statuses
    })

    return leads


def save_leads(leads: pd.DataFrame) -> None:
    """
    Save leads dataframe to data/raw/leads.csv.
    """
    project_root = Path(__file__).resolve().parents[1]
    output_path = project_root / "data" / "raw" / "leads.csv"

    output_path.parent.mkdir(parents=True, exist_ok=True)

    leads.to_csv(output_path, index=False)

    print(f"leads.csv saved to: {output_path}")
    print(f"Rows: {len(leads)}")
    print(f"Columns: {leads.shape[1]}")


if __name__ == "__main__":
    leads_df = generate_leads()
    save_leads(leads_df)