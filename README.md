# Formula 1 ETL Pipeline (1950-2025)

A comprehensive ETL (Extract, Transform, Load) pipeline for Formula 1 Championship data using Python, Polars, and BigQuery.

## Project Overview

This pipeline processes F1 racing data through 5 main stages:
1. **Setup & Environment** - Configure Python environment and dependencies
2. **Extraction** - Extract CSV data using Polars
3. **Transformation** - Clean and transform the data
4. **Load to Parquet** - Export processed data to Parquet format
5. **Load to BigQuery** - Load final data to Google BigQuery

## Project Structure

```
ETL Pipeline for F1/
├── data/
│   ├── raw/           # Raw CSV files
│   └── processed/     # Processed Parquet files
├── scripts/           # Python scripts for each step
├── config/            # Configuration files
├── requirements.txt   # Python dependencies
├── .env.example       # Environment variables template
└── README.md          # This file
```

## Setup Instructions

### 1. Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment
- Copy `.env.example` to `.env`
- Update with your BigQuery credentials and paths

### 4. Prepare Data
- Download F1 data CSV files and place in `data/raw/`

## Pipeline Steps

### Step 2: Extraction
Extract and load CSV files using Polars for efficient data handling.

### Step 3: Transformation
Clean data, handle missing values, and create necessary transformations.

### Step 4: Load to Parquet
Save transformed data in Parquet format for efficient storage.

### Step 5: Load to BigQuery
Upload Parquet data to Google BigQuery for analysis.

## Dependencies

- **polars** - Fast DataFrame library for data extraction and transformation
- **google-cloud-bigquery** - Google BigQuery client
- **pyarrow** - Arrow Python bindings for Parquet support
- **python-dotenv** - Environment variable management

## Notes

- Ensure you have BigQuery access and valid GCP credentials
- F1 data CSV files should be placed in `data/raw/`
- Processed files will be generated in `data/processed/`
