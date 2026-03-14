"""
Step 5: BigQuery Loader Module
Loads transformed data to Google BigQuery
"""
from google.cloud import bigquery
from google.oauth2 import service_account
import polars as pl
from pathlib import Path
from typing import Dict, Optional
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from config.config import GCP_PROJECT_ID, GCP_DATASET_ID, GCP_CREDENTIALS_PATH


class BigQueryLoader:
    """Load data to Google BigQuery"""
    
    def __init__(self, project_id: str = GCP_PROJECT_ID, 
                 dataset_id: str = GCP_DATASET_ID,
                 credentials_path: str = GCP_CREDENTIALS_PATH):
        """
        Initialize BigQuery loader
        
        Args:
            project_id: GCP Project ID
            dataset_id: BigQuery Dataset ID
            credentials_path: Path to service account JSON key
        """
        self.project_id = project_id
        self.dataset_id = dataset_id
        self.credentials_path = credentials_path
        self.client = None
        self.is_authenticated = False
    
    def authenticate(self) -> bool:
        """
        Authenticate with BigQuery using service account
        
        Returns:
            True if authentication successful, False otherwise
        """
        try:
            if self.credentials_path and Path(self.credentials_path).exists():
                credentials = service_account.Credentials.from_service_account_file(
                    self.credentials_path
                )
                self.client = bigquery.Client(
                    project=self.project_id,
                    credentials=credentials
                )
                print("✓ Successfully authenticated with BigQuery")
                self.is_authenticated = True
                return True
            else:
                print("⚠️  Credentials file not found. Using default authentication.")
                print("   Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set.")
                self.client = bigquery.Client(project=self.project_id)
                self.is_authenticated = True
                return True
        except Exception as e:
            print(f"✗ Authentication failed: {str(e)}")
            return False
    
    def create_dataset(self) -> bool:
        """
        Create BigQuery dataset if it doesn't exist
        
        Returns:
            True if successful, False otherwise
        """
        if not self.is_authenticated:
            print("✗ Not authenticated. Call authenticate() first.")
            return False
        
        try:
            dataset_id_full = f"{self.project_id}.{self.dataset_id}"
            dataset = bigquery.Dataset(dataset_id_full)
            dataset.location = "US"
            
            dataset = self.client.create_dataset(dataset, exists_ok=True, timeout=30)
            print(f"✓ Dataset created/exists: {self.dataset_id}")
            return True
        except Exception as e:
            print(f"✗ Error creating dataset: {str(e)}")
            return False
    
    def load_dataframe_to_bigquery(self, df: pl.DataFrame, 
                                   table_id: str,
                                   write_disposition: str = "WRITE_TRUNCATE") -> bool:
        """
        Load a Polars DataFrame to BigQuery table
        
        Args:
            df: Polars DataFrame to load
            table_id: BigQuery table name
            write_disposition: Write disposition (WRITE_TRUNCATE, WRITE_APPEND)
            
        Returns:
            True if successful, False otherwise
        """
        if not self.is_authenticated:
            print("✗ Not authenticated. Call authenticate() first.")
            return False
        
        try:
            # Convert Polars DataFrame to pandas for BigQuery
            pandas_df = df.to_pandas()
            
            full_table_id = f"{self.project_id}.{self.dataset_id}.{table_id}"
            
            job_config = bigquery.LoadJobConfig()
            job_config.write_disposition = write_disposition
            job_config.autodetect = True
            
            print(f"  Loading {len(pandas_df)} rows to {table_id}...")
            
            load_job = self.client.load_table_from_dataframe(
                pandas_df,
                full_table_id,
                job_config=job_config,
            )
            
            load_job.result()  # Wait for job to complete
            
            print(f"✓ Loaded: {table_id}")
            print(f"  Rows: {len(pandas_df)}")
            print(f"  Columns: {len(pandas_df.columns)}\n")
            return True
            
        except Exception as e:
            print(f"✗ Error loading to BigQuery: {str(e)}\n")
            return False
    
    def load_all_to_bigquery(self, dataframes: Dict[str, pl.DataFrame]) -> Dict[str, bool]:
        """
        Load all dataframes to BigQuery
        
        Args:
            dataframes: Dictionary of Polars DataFrames
            
        Returns:
            Dictionary indicating success/failure for each table
        """
        if not self.is_authenticated:
            print("✗ Not authenticated. Call authenticate() first.")
            return {}
        
        print("\n📤 Loading data to BigQuery...\n")
        
        results = {}
        
        for name, df in dataframes.items():
            success = self.load_dataframe_to_bigquery(df, name)
            results[name] = success
        
        return results


def display_bigquery_summary(results: Dict[str, bool]) -> None:
    """
    Display summary of BigQuery load operations
    
    Args:
        results: Dictionary of load results
    """
    print("\n" + "="*60)
    print("☁️  BIGQUERY LOAD SUMMARY")
    print("="*60 + "\n")
    
    successful = sum(1 for v in results.values() if v)
    failed = len(results) - successful
    
    print(f"Total Tables: {len(results)}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}\n")


if __name__ == "__main__":
    print("⚠️  This module should be imported and used from main.py")
