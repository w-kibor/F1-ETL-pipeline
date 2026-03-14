"""
Step 4: Parquet Loader Module
Loads transformed data to Parquet format
"""
import polars as pl
from pathlib import Path
from typing import Dict
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from config.config import PROCESSED_DATA_PATH


class ParquetLoader:
    """Load and save data in Parquet format"""
    
    def __init__(self, output_directory: Path = PROCESSED_DATA_PATH):
        """
        Initialize Parquet loader
        
        Args:
            output_directory: Directory to save Parquet files
        """
        self.output_directory = Path(output_directory)
        self.output_directory.mkdir(parents=True, exist_ok=True)
    
    def save_parquet(self, df: pl.DataFrame, filename: str) -> Path:
        """
        Save a Polars DataFrame to Parquet format
        
        Args:
            df: Input Polars DataFrame
            filename: Output filename (with or without .parquet extension)
            
        Returns:
            Path to saved Parquet file
        """
        if not filename.endswith('.parquet'):
            filename = f"{filename}.parquet"
        
        output_path = self.output_directory / filename
        
        try:
            df.write_parquet(output_path)
            file_size_mb = output_path.stat().st_size / (1024 * 1024)
            print(f"✓ Saved: {filename}")
            print(f"  Size: {file_size_mb:.2f} MB")
            print(f"  Path: {output_path}\n")
            return output_path
        except Exception as e:
            print(f"✗ Error saving {filename}: {str(e)}\n")
            raise
    
    def save_all_parquet(self, dataframes: Dict[str, pl.DataFrame]) -> Dict[str, Path]:
        """
        Save all dataframes to Parquet format
        
        Args:
            dataframes: Dictionary of Polars DataFrames
            
        Returns:
            Dictionary mapping df names to output paths
        """
        print("\n💾 Saving data to Parquet format...\n")
        
        saved_files = {}
        
        for name, df in dataframes.items():
            output_path = self.save_parquet(df, name)
            saved_files[name] = output_path
        
        return saved_files
    
    def load_parquet(self, filename: str) -> pl.DataFrame:
        """
        Load a Parquet file into a Polars DataFrame
        
        Args:
            filename: Parquet filename
            
        Returns:
            Polars DataFrame
        """
        if not filename.endswith('.parquet'):
            filename = f"{filename}.parquet"
        
        parquet_path = self.output_directory / filename
        
        try:
            df = pl.read_parquet(parquet_path)
            print(f"✓ Loaded: {filename}")
            print(f"  Shape: {df.shape}\n")
            return df
        except Exception as e:
            print(f"✗ Error loading {filename}: {str(e)}\n")
            raise


def display_parquet_summary(saved_files: Dict[str, Path]) -> None:
    """
    Display summary of saved Parquet files
    
    Args:
        saved_files: Dictionary of saved file paths
    """
    print("\n" + "="*60)
    print("📁 PARQUET FILES SAVED")
    print("="*60 + "\n")
    
    total_size = 0
    for name, path in saved_files.items():
        if path.exists():
            size_mb = path.stat().st_size / (1024 * 1024)
            total_size += size_mb
            print(f"✓ {name}.parquet - {size_mb:.2f} MB")
    
    print(f"\nTotal Size: {total_size:.2f} MB\n")


if __name__ == "__main__":
    print("⚠️  This module should be imported and used from main.py")
