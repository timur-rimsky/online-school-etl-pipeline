from pathlib import Path
import pandas as pd

def get_project_root() -> Path:
    return Path(__file__).resolve().parents[1]

def get_files_in_folder(folder_path: Path) -> list[Path]:
    return [
        file_path
        for file_path in folder_path.iterdir()
        if file_path.is_file() and file_path.suffix.lower() == ".csv"
    ]

def load_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)

def extract_data() -> dict[str, pd.DataFrame]:
    csv_files_path = get_project_root() / "data" / "raw"

    csv_files = get_files_in_folder(csv_files_path)

    data = {}

    for csv_file in csv_files:
        table_name = csv_file.stem
        data[table_name] = load_csv(csv_file)

    return data

if __name__ == "__main__":
    extracted_data = extract_data()

    for table_name, dataframe in extracted_data.items():
        print(f"{table_name}: {dataframe.shape}")










