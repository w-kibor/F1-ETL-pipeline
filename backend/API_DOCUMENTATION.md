# F1 ETL Pipeline Backend API Documentation

## Overview

FastAPI REST backend for the F1 ETL Pipeline. Provides endpoints for extracting, transforming, and loading F1 racing data.

## Quick Start

### Installation

1. Install dependencies:
```bash
pip install -r ../requirements.txt
```

2. Run the backend server:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

### Swagger Documentation

Interactive API documentation is available at:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## API Endpoints

### Health Check

**GET** `/health`

Check if the API is running and healthy.

**Response:**
```json
{
  "status": "healthy",
  "message": "F1 ETL Pipeline API is running"
}
```

### Pipeline Operations

#### Extract CSV Data

**POST** `/etl/extract`

Extract and load all CSV files from `data/raw/` directory.

**Response:**
```json
{
  "status": "success",
  "message": "Extracted 8 datasets",
  "data": {
    "total_files": 8,
    "datasets": {
      "drivers": {
        "rows": 857,
        "columns": 9,
        "column_names": ["driverId", "code", "forename", ...]
      }
    }
  }
}
```

#### Transform Data

**POST** `/etl/transform`

Transform and clean the extracted data. Requires extraction to be completed first.

**Response:**
```json
{
  "status": "success",
  "message": "Transformed 8 datasets",
  "data": {
    "total_transformed": 8,
    "datasets": { ... }
  }
}
```

#### Load to Parquet

**POST** `/etl/load-parquet`

Save transformed data to Parquet format. Requires transformation to be completed first.

**Response:**
```json
{
  "status": "success",
  "message": "Saved 8 Parquet files",
  "data": {
    "total_files": 8,
    "files": {
      "drivers": "/path/to/data/processed/drivers.parquet"
    }
  }
}
```

#### Run Full Pipeline

**POST** `/etl/run`

Execute the complete ETL pipeline (extract → transform → parquet) in one call.

**Response:**
```json
{
  "status": "success",
  "message": "Full ETL pipeline completed",
  "data": {
    "extracted_files": 8,
    "transformed_files": 8,
    "saved_parquet_files": 8,
    "parquet_locations": { ... }
  }
}
```

### Data Operations

#### Get Datasets Summary

**GET** `/data/datasets`

Get summary information about all extracted datasets.

**Response:**
```json
{
  "total_datasets": 8,
  "datasets": {
    "drivers": {
      "rows": 857,
      "columns": 9,
      "column_names": ["driverId", "code", ...],
      "dtypes": { "driverId": "Int64", ... }
    }
  }
}
```

#### Get Dataset Preview

**GET** `/data/preview/{dataset_name}?limit=10`

Get a preview of specific dataset (first N rows).

**Parameters:**
- `dataset_name` (string, required): Name of the dataset
- `limit` (integer, optional): Number of rows to return (default: 10)

**Response:**
```json
{
  "dataset_name": "drivers",
  "total_rows": 857,
  "preview_rows": 10,
  "data": [
    {
      "driverId": 1,
      "code": "HAM",
      "forename": "Lewis",
      "surname": "Hamilton",
      ...
    }
  ]
}
```

#### Get Pipeline Status

**GET** `/pipeline/status`

Get current execution status of the pipeline.

**Response:**
```json
{
  "extraction_complete": true,
  "transformation_complete": true,
  "parquet_export_complete": true,
  "extracted_datasets": 8,
  "transformed_datasets": 8,
  "parquet_files": 8
}
```

## Error Handling

All endpoints return appropriate HTTP status codes and error messages:

- **200**: Success
- **400**: Bad Request (e.g., missing required data)
- **404**: Not Found
- **500**: Server Error

Error response format:
```json
{
  "detail": "Error message describing what went wrong"
}
```

## Environment Variables

Create a `.env` file or set environment variables:

```env
# Backend host and port
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000

# Google Cloud / BigQuery credentials (if using BigQuery loader)
GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json
```

## Data Flow

```
CSV Files (data/raw/)
    ↓
Extract API (/etl/extract)
    ↓
Transform API (/etl/transform)
    ↓
Load Parquet API (/etl/load-parquet)
    ↓
Parquet Files (data/processed/)
    ↓
BigQuery (optional, via loader_bigquery.py)
```

## Integration with Frontend

The frontend communicates with the backend via the `ETLApiService` client:

```typescript
import { etlApi } from '@/services/etlApi';

// Run full pipeline
const result = await etlApi.runFullPipeline();

// Get datasets
const datasets = await etlApi.getDatasets();

// Get dataset preview
const preview = await etlApi.getDatasetPreview('drivers', 20);
```

## Troubleshooting

### "No CSV files found"
- Ensure CSV files are placed in `data/raw/` directory
- Check file permissions

### "No data extracted" on transform/parquet
- Run extraction first (`/etl/extract`)
- The pipeline stages must be executed in order

### CORS errors in frontend
- Backend is already configured with CORS middleware
- Ensure backend is running on the configured port
- Check frontend's `VITE_API_URL` environment variable

### Connection refused
- Ensure backend server is running: `python main.py`
- Check if port 8000 is available or configure a different port
