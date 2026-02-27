"""
Configuration module for F1 ETL Pipeline
"""
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()

# Base paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_PATH = DATA_DIR / "raw"
PROCESSED_DATA_PATH = DATA_DIR / "processed"

# BigQuery Configuration
GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID", "your-project-id")
GCP_DATASET_ID = os.getenv("GCP_DATASET_ID", "f1_racing_data")
GCP_CREDENTIALS_PATH = os.getenv("GCP_CREDENTIALS_PATH", "")

# Parquet Configuration
PARQUET_OUTPUT_PATH = PROCESSED_DATA_PATH / "f1_data.parquet"

# Ensure directories exist
RAW_DATA_PATH.mkdir(parents=True, exist_ok=True)
PROCESSED_DATA_PATH.mkdir(parents=True, exist_ok=True)

print(f"✓ Configuration loaded successfully")
print(f"  Project: {GCP_PROJECT_ID}")
print(f"  Dataset: {GCP_DATASET_ID}")
print(f"  Raw data path: {RAW_DATA_PATH}")
print(f"  Processed data path: {PROCESSED_DATA_PATH}")
