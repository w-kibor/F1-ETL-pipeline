"""
FastAPI Backend for F1 ETL Pipeline
Serves data and ETL functionality to frontend
"""
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.extraction import load_csv_files, display_dataframe_info
from scripts.transformation import F1DataTransformer
from scripts.loader_parquet import ParquetLoader

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="F1 ETL Pipeline API",
    description="REST API for Formula 1 ETL Operations",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Response Models
class PipelineStatus(BaseModel):
    status: str
    message: str
    data: Optional[Dict[str, Any]] = None

class DataSummary(BaseModel):
    dataset_name: str
    rows: int
    columns: int
    column_names: list

class PipelineProgress(BaseModel):
    step: str
    status: str
    message: str

# Global state for cached data
_cache = {
    "datasets": None,
    "transformed_datasets": None,
    "parquet_files": None
}

@app.get("/health", response_model=PipelineStatus)
def health_check():
    """Check API health"""
    logger.info("Health check requested")
    return PipelineStatus(
        status="healthy",
        message="F1 ETL Pipeline API is running"
    )

@app.post("/etl/extract", response_model=PipelineStatus)
def extract_data():
    """
    Step 1: Extract CSV files
    Loads all CSV files from data/raw directory
    """
    try:
        logger.info("Starting data extraction...")
        datasets = load_csv_files()
        
        if not datasets:
            logger.warning("No datasets found during extraction")
            raise HTTPException(status_code=400, detail="No CSV files found in data/raw/")
        
        # Cache the datasets
        _cache["datasets"] = datasets
        
        summary = {
            "total_files": len(datasets),
            "datasets": {
                name: {
                    "rows": df.shape[0],
                    "columns": df.shape[1],
                    "column_names": df.columns
                }
                for name, df in datasets.items()
            }
        }
        
        logger.info(f"Successfully extracted {len(datasets)} datasets")
        return PipelineStatus(
            status="success",
            message=f"Extracted {len(datasets)} datasets",
            data=summary
        )
    except Exception as e:
        logger.error(f"Extraction error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Extraction failed: {str(e)}")

@app.post("/etl/transform", response_model=PipelineStatus)
def transform_data():
    """
    Step 2: Transform and clean data
    Requires extraction to be completed first
    """
    try:
        if _cache["datasets"] is None:
            raise HTTPException(status_code=400, detail="No data extracted. Run /etl/extract first")
        
        logger.info("Starting data transformation...")
        transformer = F1DataTransformer(_cache["datasets"])
        transformed_datasets = transformer.transform_all()
        
        # Cache the transformed datasets
        _cache["transformed_datasets"] = transformed_datasets
        
        summary = {
            "total_transformed": len(transformed_datasets),
            "datasets": {
                name: {
                    "rows": df.shape[0],
                    "columns": df.shape[1],
                    "column_names": df.columns
                }
                for name, df in transformed_datasets.items()
            }
        }
        
        logger.info(f"Successfully transformed {len(transformed_datasets)} datasets")
        return PipelineStatus(
            status="success",
            message=f"Transformed {len(transformed_datasets)} datasets",
            data=summary
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Transformation error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Transformation failed: {str(e)}")

@app.post("/etl/load-parquet", response_model=PipelineStatus)
def load_to_parquet():
    """
    Step 3: Load transformed data to Parquet format
    Requires transformation to be completed first
    """
    try:
        if _cache["transformed_datasets"] is None:
            raise HTTPException(status_code=400, detail="No transformed data. Run /etl/transform first")
        
        logger.info("Starting Parquet export...")
        parquet_loader = ParquetLoader()
        saved_files = parquet_loader.save_all_parquet(_cache["transformed_datasets"])
        
        # Cache the files
        _cache["parquet_files"] = saved_files
        
        summary = {
            "total_files": len(saved_files),
            "files": {
                name: str(path) for name, path in saved_files.items()
            }
        }
        
        logger.info(f"Successfully saved {len(saved_files)} Parquet files")
        return PipelineStatus(
            status="success",
            message=f"Saved {len(saved_files)} Parquet files",
            data=summary
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Parquet loading error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Parquet loading failed: {str(e)}")

@app.post("/etl/run", response_model=PipelineStatus)
def run_full_pipeline():
    """
    Run complete ETL pipeline (extract -> transform -> parquet)
    """
    try:
        logger.info("Starting full ETL pipeline...")
        
        # Extract
        logger.info("Stage 1: Extraction")
        datasets = load_csv_files()
        if not datasets:
            raise HTTPException(status_code=400, detail="No CSV files found")
        _cache["datasets"] = datasets
        
        # Transform
        logger.info("Stage 2: Transformation")
        transformer = F1DataTransformer(datasets)
        transformed_datasets = transformer.transform_all()
        _cache["transformed_datasets"] = transformed_datasets
        
        # Load to Parquet
        logger.info("Stage 3: Parquet Export")
        parquet_loader = ParquetLoader()
        saved_files = parquet_loader.save_all_parquet(transformed_datasets)
        _cache["parquet_files"] = saved_files
        
        summary = {
            "extracted_files": len(datasets),
            "transformed_files": len(transformed_datasets),
            "saved_parquet_files": len(saved_files),
            "parquet_locations": {name: str(path) for name, path in saved_files.items()}
        }
        
        logger.info("Full ETL pipeline completed successfully")
        return PipelineStatus(
            status="success",
            message="Full ETL pipeline completed",
            data=summary
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Full pipeline error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Pipeline failed: {str(e)}")

@app.get("/data/datasets", response_model=Dict[str, Any])
def get_datasets():
    """Get summary of extracted datasets"""
    if _cache["datasets"] is None:
        raise HTTPException(status_code=400, detail="No data extracted yet")
    
    return {
        "total_datasets": len(_cache["datasets"]),
        "datasets": {
            name: {
                "rows": df.shape[0],
                "columns": df.shape[1],
                "column_names": df.columns,
                "dtypes": {col: str(df[col].dtype) for col in df.columns}
            }
            for name, df in _cache["datasets"].items()
        }
    }

@app.get("/data/preview/{dataset_name}")
def get_dataset_preview(dataset_name: str, limit: int = 10):
    """Get preview of a specific dataset"""
    if _cache["datasets"] is None:
        raise HTTPException(status_code=400, detail="No data extracted yet")
    
    if dataset_name not in _cache["datasets"]:
        raise HTTPException(status_code=404, detail=f"Dataset '{dataset_name}' not found")
    
    try:
        df = _cache["datasets"][dataset_name]
        preview_data = df.head(limit).to_dicts()
        return {
            "dataset_name": dataset_name,
            "total_rows": df.shape[0],
            "preview_rows": len(preview_data),
            "data": preview_data
        }
    except Exception as e:
        logger.error(f"Error previewing dataset: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Preview failed: {str(e)}")

@app.get("/pipeline/status")
def get_pipeline_status():
    """Get current pipeline execution status"""
    return {
        "extraction_complete": _cache["datasets"] is not None,
        "transformation_complete": _cache["transformed_datasets"] is not None,
        "parquet_export_complete": _cache["parquet_files"] is not None,
        "extracted_datasets": len(_cache["datasets"]) if _cache["datasets"] else 0,
        "transformed_datasets": len(_cache["transformed_datasets"]) if _cache["transformed_datasets"] else 0,
        "parquet_files": len(_cache["parquet_files"]) if _cache["parquet_files"] else 0
    }

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting F1 ETL Pipeline API Server")
    uvicorn.run(app, host="0.0.0.0", port=8000)
