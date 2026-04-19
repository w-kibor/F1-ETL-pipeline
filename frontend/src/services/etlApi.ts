/**
 * API Service for F1 ETL Pipeline Backend
 * Handles all communication with the FastAPI backend
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

interface PipelineStatus {
  status: string;
  message: string;
  data?: Record<string, any>;
}

interface DataSummary {
  dataset_name: string;
  rows: number;
  columns: number;
  column_names: string[];
}

interface PipelineProgress {
  step: string;
  status: string;
  message: string;
}

class ETLApiService {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  /**
   * Health check - verify API is running
   */
  async healthCheck(): Promise<PipelineStatus> {
    try {
      const response = await fetch(`${this.baseUrl}/health`);
      if (!response.ok) throw new Error("Health check failed");
      return await response.json();
    } catch (error) {
      console.error("Health check error:", error);
      throw error;
    }
  }

  /**
   * Extract CSV data
   */
  async extract(): Promise<PipelineStatus> {
    try {
      const response = await fetch(`${this.baseUrl}/etl/extract`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || "Extraction failed");
      }

      return await response.json();
    } catch (error) {
      console.error("Extraction error:", error);
      throw error;
    }
  }

  /**
   * Transform and clean data
   */
  async transform(): Promise<PipelineStatus> {
    try {
      const response = await fetch(`${this.baseUrl}/etl/transform`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || "Transformation failed");
      }

      return await response.json();
    } catch (error) {
      console.error("Transformation error:", error);
      throw error;
    }
  }

  /**
   * Load data to Parquet format
   */
  async loadParquet(): Promise<PipelineStatus> {
    try {
      const response = await fetch(`${this.baseUrl}/etl/load-parquet`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || "Parquet loading failed");
      }

      return await response.json();
    } catch (error) {
      console.error("Parquet loading error:", error);
      throw error;
    }
  }

  /**
   * Run complete ETL pipeline
   */
  async runFullPipeline(): Promise<PipelineStatus> {
    try {
      const response = await fetch(`${this.baseUrl}/etl/run`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || "Pipeline execution failed");
      }

      return await response.json();
    } catch (error) {
      console.error("Pipeline error:", error);
      throw error;
    }
  }

  /**
   * Get extracted datasets summary
   */
  async getDatasets(): Promise<Record<string, any>> {
    try {
      const response = await fetch(`${this.baseUrl}/data/datasets`);

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || "Failed to fetch datasets");
      }

      return await response.json();
    } catch (error) {
      console.error("Get datasets error:", error);
      throw error;
    }
  }

  /**
   * Get preview of a specific dataset
   */
  async getDatasetPreview(
    datasetName: string,
    limit: number = 10
  ): Promise<Record<string, any>> {
    try {
      const response = await fetch(
        `${this.baseUrl}/data/preview/${datasetName}?limit=${limit}`
      );

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || "Failed to fetch dataset preview");
      }

      return await response.json();
    } catch (error) {
      console.error("Get dataset preview error:", error);
      throw error;
    }
  }

  /**
   * Get current pipeline execution status
   */
  async getPipelineStatus(): Promise<Record<string, any>> {
    try {
      const response = await fetch(`${this.baseUrl}/pipeline/status`);

      if (!response.ok) {
        throw new Error("Failed to fetch pipeline status");
      }

      return await response.json();
    } catch (error) {
      console.error("Get pipeline status error:", error);
      throw error;
    }
  }
}

// Export singleton instance
export const etlApi = new ETLApiService();
export default ETLApiService;
