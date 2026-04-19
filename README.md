# Formula 1 ETL Pipeline (1950-2025)

A comprehensive ETL (Extract, Transform, Load) pipeline for Formula 1 Championship data using Python, Polars, and BigQuery.

## Project Overview

This project includes both a Python ETL pipeline and a React frontend with FastAPI backend:

**Backend Architecture:**
1. **FastAPI Server** - REST API for ETL operations
2. **Extraction** - Extract CSV data using Polars
3. **Transformation** - Clean and transform the data
4. **Load to Parquet** - Export processed data to Parquet format
5. **Load to BigQuery** - Load final data to Google BigQuery (optional)

**Frontend:** React + TypeScript with Vite, displaying F1 race data and analytics

## Project Structure

```
ETL Pipeline for F1/
├── backend/
│   ├── main.py                # FastAPI application
│   ├── API_DOCUMENTATION.md   # API endpoint documentation
│   └── __init__.py
├── frontend/
│   ├── src/
│   │   ├── app/               # React components
│   │   ├── services/
│   │   │   └── etlApi.ts      # API client
│   │   └── main.tsx
│   ├── package.json
│   ├── vite.config.ts
│   └── .env.example
├── data/
│   ├── raw/                   # Raw CSV files
│   └── processed/             # Processed Parquet files
├── scripts/
│   ├── extraction.py          # Extraction logic
│   ├── transformation.py      # Transformation logic
│   ├── loader_parquet.py      # Parquet export
│   ├── loader_bigquery.py     # BigQuery loader
│   └── main.py                # ETL orchestrator
├── config/
│   └── config.py              # Configuration
├── requirements.txt           # Python dependencies
├── .env.example               # Environment template
└── README.md                  # This file
```

## Setup Instructions

### Backend Setup

#### 1. Create Virtual Environment
```bash
python -m venv venv

# On Linux/Mac:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

#### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 3. Configure Environment
- Copy `.env.example` to `.env`
- Update with your BigQuery credentials if using BigQuery

#### 4. Prepare Data
- Download F1 data CSV files and place in `data/raw/`

#### 5. Start Backend Server
```bash
python backend/main.py
```

The API will be available at `http://localhost:8000`

- **Swagger Documentation**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Frontend Setup

#### 1. Navigate to Frontend Directory
```bash
cd frontend
```

#### 2. Install Dependencies
```bash
npm install
# or with pnpm:
pnpm install
```

#### 3. Configure Environment
```bash
# Create .env file from template
cp .env.example .env
```

Update `.env` with backend URL:
```env
VITE_API_URL=http://localhost:8000
```

#### 4. Run Development Server
```bash
npm run dev
# or with pnpm:
pnpm dev
```

The frontend will be available at `http://localhost:5173`

#### 5. Build for Production
```bash
npm run build
# or with pnpm:
pnpm build
```

## Running the Application

### Quick Start (Development)

**Terminal 1 - Backend:**
```bash
# From project root
python backend/main.py
# API available at http://localhost:8000
```

**Terminal 2 - Frontend:**
```bash
# From project root
cd frontend
npm run dev
# Frontend available at http://localhost:5173
```

### Running ETL Pipeline

#### Method 1: Via API (Recommended for frontend)
```bash
# Run full pipeline
curl -X POST http://localhost:8000/etl/run

# Or step-by-step:
curl -X POST http://localhost:8000/etl/extract
curl -X POST http://localhost:8000/etl/transform
curl -X POST http://localhost:8000/etl/load-parquet
```

#### Method 2: Directly via Python
```bash
python scripts/main.py
```

## Pipeline Operations

### API Endpoints

For complete API documentation, see [API_DOCUMENTATION.md](backend/API_DOCUMENTATION.md)

**Key Endpoints:**
- `POST /etl/extract` - Extract CSV files
- `POST /etl/transform` - Transform data
- `POST /etl/load-parquet` - Load to Parquet
- `POST /etl/run` - Run full pipeline
- `GET /data/datasets` - Get datasets summary
- `GET /data/preview/{dataset_name}` - Preview dataset
- `GET /pipeline/status` - Get pipeline status

### Step Details

### Step Details

**Extraction:** Extracts and loads CSV files using Polars for efficient data handling.

**Transformation:** Cleans data, handles missing values, and standardizes schemas.

**Load to Parquet:** Saves transformed data in Parquet format for efficient storage.

**Load to BigQuery:** (Optional) Uploads Parquet data to Google BigQuery for analysis.

## Dependencies

### Backend
- **fastapi** - FastAPI web framework for building REST APIs
- **uvicorn** - ASGI server for running FastAPI
- **pydantic** - Data validation and serialization
- **polars** - Fast DataFrame library for ETL operations
- **google-cloud-bigquery** - Google BigQuery client
- **pyarrow** - Arrow Python bindings for Parquet support
- **python-dotenv** - Environment variable management

### Frontend
- **React 18** - UI library
- **TypeScript** - Type-safe JavaScript
- **Vite** - Fast frontend build tool
- **Tailwind CSS** - Utility-first CSS framework
- **shadcn/ui** - Component library
- **Motion** - Animation library

## Notes

- Ensure you have BigQuery access and valid GCP credentials (if using BigQuery)
- F1 data CSV files should be placed in `data/raw/`
- Processed files will be generated in `data/processed/`
- Backend runs on `http://localhost:8000` by default
- Frontend runs on `http://localhost:5173` (Vite dev server)

## Troubleshooting

### Backend Issues

**"Port 8000 already in use"**
- Change the port in `backend/main.py`
- Or kill existing process: `lsof -ti:8000 | xargs kill -9`

**"No CSV files found"**
- Ensure CSV files are in `data/raw/` directory
- Check file permissions

**"Module not found" errors**
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt`

### Frontend Issues

**"API_URL not configured"**
- Create `.env` file in `frontend/` directory
- Set `VITE_API_URL=http://localhost:8000`

**"CORS errors"**
- Ensure backend is running on configured port
- Backend CORS is already configured for all origins

**"npm: command not found"**
- Install Node.js from https://nodejs.org/
- Or use pnpm: `npm install -g pnpm`

## API Documentation

Full API documentation is available at:
- [API_DOCUMENTATION.md](backend/API_DOCUMENTATION.md)
- Interactive Swagger UI: `http://localhost:8000/docs` (when backend is running)

## Performance Optimizations

- Data is cached on successful pipeline execution
- Parquet format provides efficient storage and querying
- Frontend uses lazy loading and code splitting
- React components are optimized with proper memoization

## Future Enhancements

- [ ] Add BigQuery export from frontend
- [ ] Real-time data streaming
- [ ] Advanced analytics dashboard
- [ ] Database integration (PostgreSQL/MongoDB)
- [ ] Docker containerization
- [ ] CI/CD pipeline with GitHub Actions
- [ ] Unit and integration tests
- [ ] API authentication and rate limiting
