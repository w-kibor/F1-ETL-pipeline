"""
Step 3: Data Transformation Module
Cleans and transforms Formula 1 data
"""
import polars as pl
from typing import Dict
from pathlib import Path


class F1DataTransformer:
    """Transform and clean F1 racing data"""
    
    def __init__(self, dataframes: Dict[str, pl.DataFrame]):
        """
        Initialize transformer with loaded dataframes
        
        Args:
            dataframes: Dictionary of Polars DataFrames
        """
        self.dataframes = dataframes
        self.transformed_data = {}
    
    def handle_missing_values(self, df: pl.DataFrame) -> pl.DataFrame:
        """
        Handle missing values in the dataframe
        
        Args:
            df: Input Polars DataFrame
            
        Returns:
            DataFrame with missing values handled
        """
        print(f"  - Inspecting missing values...")
        
        # Check for null values
        null_counts = df.null_count()
        
        # Fill numeric columns with 0
        numeric_cols = df.select(pl.col(pl.Int64, pl.Float64)).columns
        for col in numeric_cols:
            if null_counts[col][0] > 0:
                df = df.with_columns(pl.col(col).fill_null(0))
        
        # Fill text columns with 'Unknown'
        string_cols = df.select(pl.col(pl.Utf8)).columns
        for col in string_cols:
            if null_counts[col][0] > 0:
                df = df.with_columns(pl.col(col).fill_null("Unknown"))
        
        return df
    
    def standardize_column_names(self, df: pl.DataFrame) -> pl.DataFrame:
        """
        Standardize column names (lowercase, replace spaces with underscores)
        
        Args:
            df: Input Polars DataFrame
            
        Returns:
            DataFrame with standardized column names
        """
        new_columns = [col.lower().replace(" ", "_") for col in df.columns]
        return df.rename(dict(zip(df.columns, new_columns)))
    
    def transform_dataset(self, df: pl.DataFrame) -> pl.DataFrame:
        """
        Apply all transformations to a dataset
        
        Args:
            df: Input Polars DataFrame
            
        Returns:
            Transformed DataFrame
        """
        # Standardize column names
        df = self.standardize_column_names(df)
        
        # Handle missing values
        df = self.handle_missing_values(df)
        
        # Remove duplicates
        initial_rows = df.shape[0]
        df = df.unique()
        removed_rows = initial_rows - df.shape[0]
        if removed_rows > 0:
            print(f"  - Removed {removed_rows} duplicate rows")
        
        return df
    
    def transform_all(self) -> Dict[str, pl.DataFrame]:
        """
        Transform all loaded dataframes
        
        Returns:
            Dictionary of transformed DataFrames
        """
        print("\n🔄 Transforming data...\n")
        
        for name, df in self.dataframes.items():
            print(f"Processing: {name}")
            self.transformed_data[name] = self.transform_dataset(df)
            print(f"  ✓ Shape: {self.transformed_data[name].shape}\n")
        
        return self.transformed_data


def display_transformation_summary(original: Dict, transformed: Dict) -> None:
    """
    Display summary of transformation results
    
    Args:
        original: Original dataframes
        transformed: Transformed dataframes
    """
    print("\n" + "="*60)
    print("📈 TRANSFORMATION SUMMARY")
    print("="*60 + "\n")
    
    for name in original.keys():
        if name in transformed:
            orig_shape = original[name].shape
            trans_shape = transformed[name].shape
            print(f"{name}:")
            print(f"  Original: {orig_shape[0]} rows × {orig_shape[1]} columns")
            print(f"  Transformed: {trans_shape[0]} rows × {trans_shape[1]} columns\n")


if __name__ == "__main__":
    # This would be called from main.py with extracted data
    print("⚠️  This module should be imported and used with extracted data from extraction.py")
