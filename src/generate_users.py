from pathlib import Path

import numpy as np
import pandas as pd


def generate_users(n_users: int = 5000) -> pd.DataFrame:
    """
    Generate synthetic users data for an online school ETL project.
    Each row represents one unique user.
    """
    np.random.seed(42)

    user_ids = np.arange(1, n_users + 1)

    registration_dates = pd.to_datetime(
        np.random.choice(
            pd.date_range(start="2026-01-01", end="2026-03-31"),
            size=n_users
        )
    )

    countries = np.random.choice(
        ["Russia", "Kazakhstan", "Belarus", "Armenia"],
        size=n_users,
        p=[0.70, 0.15, 0.10, 0.05]
    )

    cities_by_country = {
        "Russia": ["Moscow", "Saint Petersburg", "Kazan", "Novosibirsk", "Rostov-on-Don"],
        "Kazakhstan": ["Almaty", "Astana", "Shymkent"],
        "Belarus": ["Minsk", "Gomel", "Brest"],
        "Armenia": ["Yerevan", "Gyumri", "Vanadzor"]
    }

    cities = [
        np.random.choice(cities_by_country[country])
        for country in countries
    ]

    ages = np.random.randint(18, 56, size=n_users)

    traffic_sources = np.random.choice(
        ["ads", "search", "social_media", "email", "referral"],
        size=n_users,
        p=[0.35, 0.25, 0.20, 0.10, 0.10]
    )

    devices = np.random.choice(
        ["mobile", "desktop", "tablet"],
        size=n_users,
        p=[0.60, 0.30, 0.10]
    )

    is_active = np.random.choice(
        [1, 0],
        size=n_users,
        p=[0.82, 0.18]
    )

    users = pd.DataFrame({
        "user_id": user_ids,
        "registration_date": registration_dates,
        "country": countries,
        "city": cities,
        "age": ages,
        "traffic_source": traffic_sources,
        "device": devices,
        "is_active": is_active
    })

    return users


def save_users(users: pd.DataFrame) -> None:
    """
    Save users dataframe to data/raw/users.csv.
    """
    project_root = Path(__file__).resolve().parents[1]
    output_path = project_root / "data" / "raw" / "users.csv"

    output_path.parent.mkdir(parents=True, exist_ok=True)

    users.to_csv(output_path, index=False)

    print(f"users.csv saved to: {output_path}")
    print(f"Rows: {len(users)}")
    print(f"Columns: {users.shape[1]}")


if __name__ == "__main__":
    users_df = generate_users()
    save_users(users_df)