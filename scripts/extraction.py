"""
Step 2: Data Extraction Module
Extracts Formula 1 data from CSV files using Polars
"""
import polars as pl
from pathlib import Path
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
    
    print(f"\n📊 Extracting data from {len(csv_files)} CSV files...\n")
    
    for csv_file in csv_files:
        try:
            df = pl.read_csv(csv_file)
            dataframe_name = csv_file.stem
            dataframes[dataframe_name] = df
            print(f"✓ Loaded: {csv_file.name}")
            print(f"  Shape: {df.shape[0]} rows × {df.shape[1]} columns\n")
        except Exception as e:
            print(f"✗ Error loading {csv_file.name}: {str(e)}\n")
    
    return dataframes


def display_dataframe_info(dataframes: dict) -> None:
    """
    Display information about loaded dataframes
    
    Args:
        dataframes: Dictionary of Polars DataFrames
    """
    print("\n" + "="*60)
    print("📋 DATAFRAME SUMMARY")
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
        print(f"✓ Successfully loaded {len(datasets)} dataset(s)")
    else:
        print("⚠️  No datasets loaded. Please add CSV files to the data/raw directory.")
