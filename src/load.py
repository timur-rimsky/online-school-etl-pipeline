from pathlib import Path
import sqlite3

import pandas as pd

from extract import extract_data
from transform import transform_data


def get_project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def get_database_path() -> Path:
    output_path = get_project_root() / "database" / "online_school.db"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    return output_path


def load_table(
    table: pd.DataFrame,
    table_name: str,
    connection: sqlite3.Connection
) -> None:
    table.to_sql(
        name=table_name,
        con=connection,
        if_exists="replace",
        index=False
    )


def load_data(data: dict[str, pd.DataFrame]) -> None:
    database_path = get_database_path()

    with sqlite3.connect(database_path) as connection:
        for table_name, dataframe in data.items():
            load_table(dataframe, table_name, connection)
            print(f"Loaded table {table_name}: {len(dataframe)} rows")

    print(f"Database saved to: {database_path}")


def check_loaded_tables() -> None:
    database_path = get_database_path()

    with sqlite3.connect(database_path) as connection:
        query = """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            ORDER BY name;
        """

        tables = pd.read_sql_query(query, connection)

    print("\nLoaded tables:\n", tables)


if __name__ == "__main__":
    raw_data = extract_data()
    cleaned_data = transform_data(raw_data)
    load_data(cleaned_data)

    check_loaded_tables()
