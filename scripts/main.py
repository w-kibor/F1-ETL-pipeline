"""
Main ETL Pipeline Orchestrator
Coordinates all 5 steps of the F1 ETL pipeline
"""
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.extraction import load_csv_files, display_dataframe_info
from scripts.transformation import F1DataTransformer, display_transformation_summary
from scripts.loader_parquet import ParquetLoader, display_parquet_summary
from scripts.loader_bigquery import BigQueryLoader, display_bigquery_summary


def run_etl_pipeline(use_bigquery: bool = False) -> bool:
    """
    Run the complete ETL pipeline
    
    Args:
        use_bigquery: Whether to load to BigQuery (requires credentials)
        
    Returns:
        True if pipeline completes successfully
    """
    print("\n" + "="*60)
    print("🚀 FORMULA 1 ETL PIPELINE")
    print("="*60 + "\n")
    
    try:
        # STEP 2: EXTRACTION
        print("📊 STEP 2: DATA EXTRACTION")
        print("-" * 60)
        datasets = load_csv_files()
        
        if not datasets:
            print("⚠️  No datasets found. Please add CSV files to data/raw/")
            return False
        
        display_dataframe_info(datasets)
        
        # STEP 3: TRANSFORMATION
        print("\n🔄 STEP 3: DATA TRANSFORMATION")
        print("-" * 60)
        transformer = F1DataTransformer(datasets)
        transformed_datasets = transformer.transform_all()
        display_transformation_summary(datasets, transformed_datasets)
        
        # STEP 4: LOAD TO PARQUET
        print("\n💾 STEP 4: LOAD TO PARQUET")
        print("-" * 60)
        parquet_loader = ParquetLoader()
        saved_files = parquet_loader.save_all_parquet(transformed_datasets)
        display_parquet_summary(saved_files)
        
        # STEP 5: LOAD TO BIGQUERY (Optional)
        if use_bigquery:
            print("\n☁️  STEP 5: LOAD TO BIGQUERY")
            print("-" * 60)
            bigquery_loader = BigQueryLoader()
            
            if bigquery_loader.authenticate():
                if bigquery_loader.create_dataset():
                    results = bigquery_loader.load_all_to_bigquery(transformed_datasets)
                    display_bigquery_summary(results)
                else:
                    print("⚠️  Could not create BigQuery dataset. Skipping BigQuery load.")
            else:
                print("⚠️  BigQuery authentication failed. Skipping BigQuery load.")
        else:
            print("\n⏭️  STEP 5: BIGQUERY LOAD - SKIPPED")
            print("(Use use_bigquery=True to enable)\n")
        
        # Summary
        print("\n" + "="*60)
        print("✓ ETL PIPELINE COMPLETED SUCCESSFULLY!")
        print("="*60 + "\n")
        
        return True
        
    except Exception as e:
        print(f"\n✗ ETL Pipeline failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    # Run pipeline without BigQuery by default
    # Set to True to enable BigQuery loading
    success = run_etl_pipeline(use_bigquery=False)
    
    sys.exit(0 if success else 1)
