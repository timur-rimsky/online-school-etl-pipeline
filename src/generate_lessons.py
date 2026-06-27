from pathlib import Path

import numpy as np
import pandas as pd


def generate_lessons() -> pd.DataFrame:
    """
    Generate synthetic lessons attendance data for an online school ETL project.
    Lessons are generated only for users with paid payments.
    Each row represents one lesson attendance event.
    """
    np.random.seed(42)

    project_root = Path(__file__).resolve().parents[1]

    payments_path = project_root / "data" / "raw" / "payments.csv"
    courses_path = project_root / "data" / "raw" / "courses.csv"

    payments = pd.read_csv(payments_path)
    courses = pd.read_csv(courses_path)

    paid_payments = payments[payments["payment_status"] == "paid"].copy()

    paid_payments["payment_date"] = pd.to_datetime(paid_payments["payment_date"])

    course_durations = courses.set_index("course_id")["duration_weeks"]

    lessons_data = []
    lesson_id = 1

    lesson_types = ["webinar", "practice", "homework_review", "consultation"]

    for _, payment in paid_payments.iterrows():
        user_id = payment["user_id"]
        course_id = payment["course_id"]
        payment_date = payment["payment_date"]

        duration_weeks = course_durations.loc[course_id]

        n_lessons = duration_weeks

        for lesson_number in range(n_lessons):
            lesson_date = payment_date + pd.Timedelta(days=7 * lesson_number)

            lesson_type = np.random.choice(
                lesson_types,
                p=[0.45, 0.30, 0.20, 0.05]
            )

            attendance_status = np.random.choice(
                ["attended", "missed", "cancelled"],
                p=[0.78, 0.17, 0.05]
            )

            lessons_data.append({
                "lesson_id": lesson_id,
                "user_id": user_id,
                "course_id": course_id,
                "lesson_date": lesson_date,
                "lesson_type": lesson_type,
                "attendance_status": attendance_status
            })

            lesson_id += 1

    lessons = pd.DataFrame(lessons_data)

    return lessons


def save_lessons(lessons: pd.DataFrame) -> None:
    """
    Save lessons dataframe to data/raw/lessons.csv.
    """
    project_root = Path(__file__).resolve().parents[1]
    output_path = project_root / "data" / "raw" / "lessons.csv"

    output_path.parent.mkdir(parents=True, exist_ok=True)

    lessons.to_csv(output_path, index=False)

    print(f"lessons.csv saved to: {output_path}")
    print(f"Rows: {len(lessons)}")
    print(f"Columns: {lessons.shape[1]}")


if __name__ == "__main__":
    lessons_df = generate_lessons()
    save_lessons(lessons_df)