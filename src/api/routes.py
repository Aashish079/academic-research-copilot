"""
FastAPI routes for Academic Research Copilot API.

This module defines the REST API endpoints for searching academic papers
using semantic search powered by MindsDB Knowledge Base.

Endpoints:
    Health Check:
        - GET /health: API health status
    
    Search:
        - POST /search: Basic semantic search with query string
        - POST /search/semantic: Semantic search with relevance threshold
        - POST /search/hybrid: Hybrid search with metadata filters
        - GET /papers/{entry_id}: Get specific paper by ID

Features:
    - Pydantic request/response validation
    - Comprehensive error handling with specific HTTP status codes
    - Input validation and sanitization
    - Async operations for better performance

Example:
    >>> # Search for papers
    >>> POST /api/search
    >>> {
    >>>     "query": "machine learning",
    >>>     "limit": 10
    >>> }
"""
from fastapi import APIRouter, HTTPException
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import date

from src.knowledge_base.queries import (
    query_academic_papers,
    semantic_search,
    hybrid_search
)
from src.utils.constants import (
    DEFAULT_SEARCH_LIMIT,
    MAX_SEARCH_LIMIT,
    MIN_SEARCH_LIMIT,
    DEFAULT_RELEVANCE_THRESHOLD,
    MIN_RELEVANCE_THRESHOLD,
    MAX_RELEVANCE_THRESHOLD,
    MAX_QUERY_LENGTH,
    MIN_QUERY_LENGTH,
    ERROR_EMPTY_QUERY,
    ERROR_INVALID_THRESHOLD,
    ERROR_INVALID_ENTRY_ID,
    ERROR_PAPER_NOT_FOUND,
    ERROR_SEARCH_FAILED,
    HTTP_BAD_REQUEST,
    HTTP_NOT_FOUND,
    HTTP_INTERNAL_ERROR,
)

# Create routers
health_router = APIRouter()
search_router = APIRouter()


# Request/Response Models
class SearchRequest(BaseModel):
    """Request model for search operations"""
    query: str = Field(..., min_length=MIN_QUERY_LENGTH, max_length=MAX_QUERY_LENGTH, description="Search query")
    limit: int = Field(default=DEFAULT_SEARCH_LIMIT, ge=MIN_SEARCH_LIMIT, le=MAX_SEARCH_LIMIT, description="Maximum number of results")
    

class SemanticSearchRequest(BaseModel):
    """Request model for semantic search"""
    query: str = Field(..., min_length=MIN_QUERY_LENGTH, max_length=MAX_QUERY_LENGTH, description="Search query")
    threshold: float = Field(default=DEFAULT_RELEVANCE_THRESHOLD, ge=MIN_RELEVANCE_THRESHOLD, le=MAX_RELEVANCE_THRESHOLD, description="Similarity threshold")


class HybridSearchRequest(BaseModel):
    """Request model for hybrid search"""
    query: str = Field(..., min_length=MIN_QUERY_LENGTH, max_length=MAX_QUERY_LENGTH, description="Search query")
    metadata_filters: Optional[Dict[str, Any]] = Field(
        default=None, 
        description="Metadata filters (e.g., {'authors': 'John Doe', 'year': 2023})"
    )
    limit: int = Field(default=DEFAULT_SEARCH_LIMIT, ge=MIN_SEARCH_LIMIT, le=MAX_SEARCH_LIMIT, description="Maximum number of results")


class PaperResponse(BaseModel):
    """Response model for a single paper"""
    entry_id: str
    title: str
    summary: str
    authors: str
    published_date: Optional[date] = None
    pdf_url: Optional[str] = None
    relevance_score: Optional[float] = None


class SearchResponse(BaseModel):
    """Response model for search results"""
    query: str
    results: List[PaperResponse]
    total_results: int
    

class HealthResponse(BaseModel):
    """Response model for health check"""
    status: str
    message: str


# Health Check Endpoint
@health_router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint to verify API is running
    """
    return HealthResponse(
        status="healthy",
        message="Academic Research Copilot API is running"
    )


# Search Endpoints
@search_router.post("/search", response_model=SearchResponse)
async def search_papers(request: SearchRequest):
    """
    Search academic papers using basic query
    
    - **query**: The search query string
    - **limit**: Maximum number of results to return (1-100)
    """
    try:
        # Validate input
        if not request.query or not request.query.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        results = await query_academic_papers(request.query, request.limit)
        
        papers = [
            PaperResponse(
                entry_id=paper.get("entry_id", ""),
                title=paper.get("title", ""),
                summary=paper.get("summary", ""),
                authors=paper.get("authors", ""),
                published_date=paper.get("published_date"),
                pdf_url=paper.get("pdf_url"),
                relevance_score=paper.get("relevance_score")
            )
            for paper in results
        ]
        
        return SearchResponse(
            query=request.query,
            results=papers,
            total_results=len(papers)
        )
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
    except Exception as e:
        # Log the error for debugging
        print(f"Error in search endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


@search_router.post("/search/semantic", response_model=SearchResponse)
async def semantic_search_papers(request: SemanticSearchRequest):
    """
    Perform semantic search on academic papers
    
    - **query**: The search query string
    - **threshold**: Minimum similarity score (0.0-1.0)
    """
    try:
        # Validate input
        if not request.query or not request.query.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        if not 0.0 <= request.threshold <= 1.0:
            raise HTTPException(status_code=400, detail="Threshold must be between 0.0 and 1.0")
        
        results = await semantic_search(request.query, request.threshold)
        
        papers = [
            PaperResponse(
                entry_id=paper.get("entry_id", ""),
                title=paper.get("title", ""),
                summary=paper.get("summary", ""),
                authors=paper.get("authors", ""),
                published_date=paper.get("published_date"),
                pdf_url=paper.get("pdf_url"),
                relevance_score=paper.get("relevance_score")
            )
            for paper in results
        ]
        
        return SearchResponse(
            query=request.query,
            results=papers,
            total_results=len(papers)
        )
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
    except Exception as e:
        print(f"Error in semantic search endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Semantic search failed: {str(e)}")


@search_router.post("/search/hybrid", response_model=SearchResponse)
async def hybrid_search_papers(request: HybridSearchRequest):
    """
    Perform hybrid search combining semantic and metadata filtering
    
    - **query**: The search query string
    - **metadata_filters**: Dictionary of metadata filters to apply
    - **limit**: Maximum number of results to return (1-100)
    """
    try:
        # Validate input
        if not request.query or not request.query.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        results = await hybrid_search(request.query, request.metadata_filters)
        
        # Apply limit
        results = results[:request.limit]
        
        papers = [
            PaperResponse(
                entry_id=paper.get("entry_id", ""),
                title=paper.get("title", ""),
                summary=paper.get("summary", ""),
                authors=paper.get("authors", ""),
                published_date=paper.get("published_date"),
                pdf_url=paper.get("pdf_url"),
                relevance_score=paper.get("relevance_score")
            )
            for paper in results
        ]
        
        return SearchResponse(
            query=request.query,
            results=papers,
            total_results=len(papers)
        )
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
    except Exception as e:
        print(f"Error in hybrid search endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Hybrid search failed: {str(e)}")


@search_router.get("/papers/{entry_id}", response_model=PaperResponse)
async def get_paper_by_id_endpoint(entry_id: str):
    """
    Get a specific paper by its entry ID
    
    - **entry_id**: The unique identifier of the paper
    """
    try:
        # Validate entry_id
        if not entry_id or not entry_id.strip():
            raise HTTPException(status_code=400, detail="Entry ID cannot be empty")
        
        from src.knowledge_base.queries import get_paper_by_id
        paper = await get_paper_by_id(entry_id.strip())
        
        if not paper:
            raise HTTPException(status_code=404, detail=f"Paper with ID '{entry_id}' not found")
        
        return PaperResponse(
            entry_id=paper.get("entry_id", ""),
            title=paper.get("title", ""),
            summary=paper.get("summary", ""),
            authors=paper.get("authors", ""),
            published_date=paper.get("published_date"),
            pdf_url=paper.get("pdf_url")
        )
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid entry ID: {str(e)}")
    except Exception as e:
        print(f"Error in get_paper_by_id endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve paper: {str(e)}")
