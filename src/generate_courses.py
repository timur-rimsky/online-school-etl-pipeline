from pathlib import Path

import pandas as pd


def generate_courses() -> pd.DataFrame:
    """
    Generate synthetic courses data for an online school ETL project.
    Each row represents one course.
    """
    courses = pd.DataFrame({
        "course_id": [1, 2, 3, 4, 5, 6],
        "course_name": [
            "Python Basics",
            "SQL for Data Analysis",
            "Machine Learning Starter",
            "Data Engineering Basics",
            "Power BI Fundamentals",
            "AI Tools for Business"
        ],
        "category": [
            "Programming",
            "Data Analytics",
            "Machine Learning",
            "Data Engineering",
            "BI",
            "Artificial Intelligence"
        ],
        "course_price": [
            12900,
            9900,
            19900,
            21900,
            14900,
            17900
        ],
        "duration_weeks": [
            8,
            6,
            10,
            12,
            7,
            8
        ]
    })

    return courses


def save_courses(courses: pd.DataFrame) -> None:
    """
    Save courses dataframe to data/raw/courses.csv.
    """
    project_root = Path(__file__).resolve().parents[1]
    output_path = project_root / "data" / "raw" / "courses.csv"

    output_path.parent.mkdir(parents=True, exist_ok=True)

    courses.to_csv(output_path, index=False)

    print(f"courses.csv saved to: {output_path}")
    print(f"Rows: {len(courses)}")
    print(f"Columns: {courses.shape[1]}")


if __name__ == "__main__":
    courses_df = generate_courses()
    save_courses(courses_df)