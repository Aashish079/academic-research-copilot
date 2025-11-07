"""
Application-wide constants and configuration values.

This module defines constants used across the application for validation,
limits, and default values to maintain consistency and ease of maintenance.
"""

# Search Configuration
DEFAULT_SEARCH_LIMIT = 10
MAX_SEARCH_LIMIT = 100
MIN_SEARCH_LIMIT = 1

# Semantic Search Thresholds
DEFAULT_RELEVANCE_THRESHOLD = 0.7
MIN_RELEVANCE_THRESHOLD = 0.0
MAX_RELEVANCE_THRESHOLD = 1.0

# Query Constraints
MAX_QUERY_LENGTH = 500
MIN_QUERY_LENGTH = 1

# Distance to Relevance Conversion
# MindsDB returns distance where 0 = perfect match
# We convert to relevance score where 1.0 = perfect match
MAX_DISTANCE_FOR_NORMALIZATION = 2.0

# Paper Metadata Defaults
DEFAULT_RELEVANCE_SCORE_FALLBACK = 0.75  # For text-based search fallback
DEFAULT_RELEVANCE_SCORE_HYBRID = 0.85    # For hybrid search fallback
DEFAULT_RELEVANCE_SCORE_SAMPLE = 0.95    # For sample data

# API Response Codes
HTTP_BAD_REQUEST = 400
HTTP_NOT_FOUND = 404
HTTP_INTERNAL_ERROR = 500

# Database Configuration
DEFAULT_DB_NAME = "duckdb_papers"
DEFAULT_KB_NAME = "academic_kb"
DEFAULT_DUCKDB_PATH = "data/academic_papers.duckdb"
CONTAINER_DUCKDB_PATH = "/app/data/academic_papers.duckdb"

# ArXiv Configuration
DEFAULT_ARXIV_DELAY = 3
DEFAULT_ARXIV_PAGE_SIZE = 50
DEFAULT_ARXIV_RETRIES = 5

# Embedding Configuration
GEMINI_EMBEDDING_MODEL = "text-embedding-004"
GEMINI_EMBEDDING_DIMENSIONS = 768

# Error Messages
ERROR_EMPTY_QUERY = "Query cannot be empty"
ERROR_INVALID_THRESHOLD = "Threshold must be between 0.0 and 1.0"
ERROR_INVALID_ENTRY_ID = "Entry ID cannot be empty"
ERROR_PAPER_NOT_FOUND = "Paper with ID '{}' not found"
ERROR_SEARCH_FAILED = "Search failed: {}"

# Success Messages
SUCCESS_PAPERS_FOUND = "✓ Found {} papers"
SUCCESS_SEMANTIC_MATCH = "✓ Found {} papers semantically similar to '{}'"
SUCCESS_FILTERED_RESULTS = "✓ Found {} papers with filters"
SUCCESS_KB_CREATED = "✅ Knowledge Base '{}' created successfully!"
SUCCESS_PAPERS_INSERTED = "✅ Papers inserted successfully into Knowledge Base!"

# Warning Messages
WARNING_KB_ERROR = "⚠️  Error querying Knowledge Base: {}"
WARNING_FALLBACK_DUCKDB = "⚠️  Falling back to DuckDB text search..."
WARNING_FALLBACK_SAMPLE = "⚠️  Returning sample data for demo purposes..."
