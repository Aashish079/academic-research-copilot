# Configuration settings for connecting to MindsDB

from pydantic_settings import BaseSettings
from functools import lru_cache
import os
from typing import Optional


class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    # MindsDB Configuration
    mindsdb_host: str = "localhost"
    mindsdb_port: int = 47334
    mindsdb_user: str = "mindsdb"
    mindsdb_password: str = ""
    mindsdb_database: str = "mindsdb"
    
    # DuckDB Configuration
    duckdb_path: str = "data/academic_papers.duckdb"
    
    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_reload: bool = True
    
    # Streamlit Configuration
    streamlit_host: str = "0.0.0.0"
    streamlit_port: int = 8501
    
    # Knowledge Base Configuration
    kb_name: str = "academic_kb"
    db_name: str = "duckdb_papers"
    
    # ArXiv API Configuration
    arxiv_delay_seconds: int = 3
    arxiv_page_size: int = 50
    arxiv_num_retries: int = 5
    
    # Google Gemini API Configuration
    gemini_api_key: Optional[str] = None
    
    @property
    def mindsdb_url(self) -> str:
        """Get full MindsDB URL"""
        return f"http://{self.mindsdb_host}:{self.mindsdb_port}"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        # Map environment variables with different names
        fields = {
            'gemini_api_key': {'env': 'GEMINI_API_KEY'},
            'duckdb_path': {'env': 'DUCKDB_PATH'},
            'arxiv_delay_seconds': {'env': 'ARXIV_DELAY_SECONDS'},
            'arxiv_page_size': {'env': 'ARXIV_PAGE_SIZE'},
            'arxiv_num_retries': {'env': 'ARXIV_NUM_RETRIES'},
        }


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()


# Legacy constants for backward compatibility
MINDSDB_HOST = os.getenv("MINDSDB_HOST", "localhost")
MINDSDB_PORT = int(os.getenv("MINDSDB_PORT", "47334"))
MINDSDB_USER = os.getenv("MINDSDB_USER", "mindsdb")
MINDSDB_PASSWORD = os.getenv("MINDSDB_PASSWORD", "")
MINDSDB_DATABASE = os.getenv("MINDSDB_DATABASE", "mindsdb")