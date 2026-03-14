"""
Step 2: Data Extraction Module
Extracts Formula 1 data from CSV files using Polars
"""
import polars as pl
from pathlib import Path
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config.config import RAW_DATA_PATH


def load_csv_files(directory: Path = RAW_DATA_PATH) -> dict:
    """
    Load all CSV files from the raw data directory
    
    Args:
        directory: Path to directory containing CSV files
        
    Returns:
        Dictionary with dataframe names as keys and Polars DataFrames as values
    """
    dataframes = {}
    
    if not directory.exists():
        print(f"Warning: Directory {directory} does not exist")
        return dataframes
    
    csv_files = list(directory.glob("*.csv"))
    
    if not csv_files:
        print(f"No CSV files found in {directory}")
        return dataframes
    
    print(f"\n[EXTRACTING] Loading {len(csv_files)} CSV files...\n")
    
    for csv_file in csv_files:
        try:
            df = pl.read_csv(
                csv_file,
                encoding="utf-8-sig",
                infer_schema_length=10000,
                ignore_errors=True
            )
            dataframe_name = csv_file.stem
            dataframes[dataframe_name] = df
            print(f"[OK] Loaded: {csv_file.name}")
            print(f"  Shape: {df.shape[0]} rows x {df.shape[1]} columns\n")
        except Exception as e:
            # Try alternative encoding if utf-8 fails
            try:
                df = pl.read_csv(
                    csv_file,
                    encoding="latin-1",
                    infer_schema_length=10000,
                    ignore_errors=True
                )
                dataframe_name = csv_file.stem
                dataframes[dataframe_name] = df
                print(f"[OK] Loaded: {csv_file.name} (with latin-1 encoding)")
                print(f"  Shape: {df.shape[0]} rows x {df.shape[1]} columns\n")
            except Exception as e2:
                print(f"[ERROR] Error loading {csv_file.name}: {str(e)}\n")
    
    return dataframes


def display_dataframe_info(dataframes: dict) -> None:
    """
    Display information about loaded dataframes
    
    Args:
        dataframes: Dictionary of Polars DataFrames
    """
    print("\n" + "="*60)
    print("[INFO] DATAFRAME SUMMARY")
    print("="*60 + "\n")
    
    for name, df in dataframes.items():
        print(f"Dataset: {name}")
        print(f"  Shape: {df.shape}")
        print(f"  Columns: {', '.join(df.columns)}")
        print(f"  Data Types: {dict(zip(df.columns, df.dtypes))}\n")


if __name__ == "__main__":
    # Load all CSV files
    datasets = load_csv_files()
    
    # Display information
    if datasets:
        display_dataframe_info(datasets)
        print(f"[OK] Successfully loaded {len(datasets)} dataset(s)")
    else:
        print("[WARNING] No datasets loaded. Please add CSV files to the data/raw directory.")
