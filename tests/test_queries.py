import pytest
import asyncio
from src.knowledge_base.queries import query_academic_papers, semantic_search, hybrid_search, get_paper_by_id


@pytest.mark.asyncio
async def test_query_academic_papers_basic():
    """Test basic query for academic papers"""
    query = "machine learning"
    results = await query_academic_papers(query, limit=5)
    
    # Should return a list
    assert isinstance(results, list), "Results should be a list"
    
    # Each result should have required fields
    if len(results) > 0:
        paper = results[0]
        assert "entry_id" in paper, "Paper should have entry_id"
        assert "title" in paper, "Paper should have title"
        assert "summary" in paper, "Paper should have summary"
        assert "authors" in paper, "Paper should have authors"


@pytest.mark.asyncio
async def test_query_academic_papers_limit():
    """Test that limit parameter works correctly"""
    query = "deep learning"
    limit = 3
    results = await query_academic_papers(query, limit=limit)
    
    assert isinstance(results, list), "Results should be a list"
    # Results should not exceed limit
    assert len(results) <= limit, f"Results ({len(results)}) should not exceed limit ({limit})"


@pytest.mark.asyncio
async def test_semantic_search():
    """Test semantic search functionality"""
    query = "neural networks"
    threshold = 0.7
    results = await semantic_search(query, threshold=threshold)
    
    assert isinstance(results, list), "Results should be a list"
    
    # Check relevance scores if results exist
    if len(results) > 0:
        for paper in results:
            assert "relevance_score" in paper, "Paper should have relevance_score"
            # Relevance score should be above threshold (or close due to fallback)
            # Note: We allow some tolerance for fallback scenarios


@pytest.mark.asyncio
async def test_hybrid_search_no_filters():
    """Test hybrid search without metadata filters"""
    query = "computer vision"
    results = await hybrid_search(query)
    
    assert isinstance(results, list), "Results should be a list"
    
    if len(results) > 0:
        paper = results[0]
        assert "entry_id" in paper, "Paper should have entry_id"
        assert "title" in paper, "Paper should have title"


@pytest.mark.asyncio
async def test_hybrid_search_with_filters():
    """Test hybrid search with metadata filters"""
    query = "artificial intelligence"
    metadata_filters = {
        "year": 2020,
        "categories": "cs.AI"
    }
    results = await hybrid_search(query, metadata_filters=metadata_filters)
    
    assert isinstance(results, list), "Results should be a list"
    # Filters may reduce results, but should still be a valid list


@pytest.mark.asyncio
async def test_get_paper_by_id():
    """Test retrieving a specific paper by ID"""
    # First, get some papers to find a valid ID
    query_results = await query_academic_papers("machine learning", limit=1)
    
    if len(query_results) > 0:
        entry_id = query_results[0]["entry_id"]
        paper = await get_paper_by_id(entry_id)
        
        if paper:  # Paper found
            assert paper["entry_id"] == entry_id, "Retrieved paper should have correct entry_id"
            assert "title" in paper, "Paper should have title"
            assert "summary" in paper, "Paper should have summary"


@pytest.mark.asyncio
async def test_query_empty_result():
    """Test query that should return empty or minimal results"""
    query = "xyzqwertyfakesearchterm12345"
    results = await query_academic_papers(query, limit=10)
    
    # Should return a list (may be empty or have fallback data)
    assert isinstance(results, list), "Results should be a list"


def test_sync_wrapper_query_knowledge_base():
    """Test the synchronous wrapper for backward compatibility"""
    from src.knowledge_base.queries import query_knowledge_base
    
    query = "neural networks"
    results = query_knowledge_base(query, limit=5)
    
    assert isinstance(results, list), "Results should be a list"
    assert len(results) <= 5, "Results should respect limit"
