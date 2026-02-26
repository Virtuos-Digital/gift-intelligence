"""
FastAPI Embedding Service - Transformer Only
Pure text-to-vector conversion service (NO vector database)
Model: MiniLM-L6-v2 (384-dimensional embeddings)
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
from sentence_transformers import SentenceTransformer
import time
from contextlib import asynccontextmanager

# ============================================================================
# Configuration
# ============================================================================
MODEL_PATH = "minilm_full_dimension_models/minilm_model"

# Global variable for model
model = None


# ============================================================================
# Startup & Shutdown Events
# ============================================================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load model on startup, cleanup on shutdown"""
    global model
    
    print("="*80)
    print("🚀 STARTING EMBEDDING SERVICE API")
    print("="*80)
    
    # Load MiniLM model
    print(f"\n📦 Loading MiniLM model from: {MODEL_PATH}")
    start_time = time.time()
    model = SentenceTransformer(MODEL_PATH)
    print(f"✓ Model loaded in {time.time() - start_time:.2f}s")
    print(f"   Embedding dimension: 384D")
    print(f"   Max sequence length: 256 tokens")
    
    print("\n✅ Embedding Service Ready!")
    print("="*80)
    
    yield
    
    # Cleanup
    print("\n🛑 Shutting down...")
    model = None


# ============================================================================
# FastAPI App
# ============================================================================
app = FastAPI(
    title="Text Embedding Service",
    description="Convert text to 384-dimensional vectors using MiniLM-L6-v2",
    version="2.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# Pydantic Models
# ============================================================================
class EmbedRequest(BaseModel):
    """Request model for embedding generation"""
    texts: List[str] = Field(
        ..., 
        min_items=1, 
        max_items=100,
        description="List of text strings to embed (max 100 per request)"
    )
    normalize: bool = Field(
        True, 
        description="Whether to normalize embeddings to unit length"
    )


class EmbeddingResult(BaseModel):
    """Single embedding result"""
    text: str
    embedding: List[float]
    tokens: Optional[int] = None


class EmbedResponse(BaseModel):
    """Response model for embedding generation"""
    embeddings: List[EmbeddingResult]
    count: int
    dimension: int
    model: str = "sentence-transformers/all-MiniLM-L6-v2"
    processing_time_ms: float


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    model_loaded: bool
    model_name: str
    embedding_dimension: int
    max_sequence_length: int


# ============================================================================
# API Endpoints
# ============================================================================
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information"""
    return {
        "service": "Text Embedding Service",
        "model": "MiniLM-L6-v2",
        "version": "2.0.0",
        "description": "Convert text to 384-dimensional semantic vectors",
        "endpoints": {
            "health": "/health",
            "embed": "/api/v1/embed",
            "model_info": "/api/v1/model-info",
            "docs": "/docs"
        }
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy" if model else "unhealthy",
        model_loaded=model is not None,
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        embedding_dimension=384,
        max_sequence_length=256
    )


@app.post("/api/v1/embed", response_model=EmbedResponse, tags=["Embeddings"])
async def generate_embeddings(request: EmbedRequest):
    """
    Generate embeddings for a list of text strings
    
    **Input:**
    - texts: List of 1-100 text strings
    - normalize: Whether to L2-normalize embeddings (recommended: True)
    
    **Output:**
    - 384-dimensional vectors for each input text
    - Processing time in milliseconds
    
    """
    if not model:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    # Validate input
    if len(request.texts) == 0:
        raise HTTPException(status_code=400, detail="No texts provided")
    
    if len(request.texts) > 100:
        raise HTTPException(
            status_code=400, 
            detail="Maximum 100 texts per request. Use batch processing for larger sets."
        )
    
    start_time = time.time()
    
    try:
        # Generate embeddings
        embeddings = model.encode(
            request.texts,
            normalize_embeddings=request.normalize,
            show_progress_bar=False,
            convert_to_numpy=True
        )
        
        # Build results
        results = []
        for text, embedding in zip(request.texts, embeddings):
            results.append(EmbeddingResult(
                text=text[:100] + "..." if len(text) > 100 else text,  # Truncate long text in response
                embedding=embedding.tolist()
            ))
        
        processing_time = (time.time() - start_time) * 1000  # Convert to ms
        
        return EmbedResponse(
            embeddings=results,
            count=len(results),
            dimension=384,
            processing_time_ms=round(processing_time, 2)
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Embedding generation failed: {str(e)}"
        )


@app.get("/api/v1/model-info", tags=["Info"])
async def get_model_info():
    """Get detailed model information"""
    if not model:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    return {
        "model_name": "sentence-transformers/all-MiniLM-L6-v2",
        "model_type": "Sentence Transformer",
        "base_model": "nreimers/MiniLM-L6-H384-uncased",
        "embedding_dimension": 384,
        "max_sequence_length": 256,  # tokens
        "max_input_length": "~512 words",
        "normalization": "L2 normalization recommended",
        "training_data": {
            "total_pairs": "1.17 billion sentence pairs",
            "datasets": [
                "Reddit comments (726M)",
                "S2ORC citations (116M)",
                "WikiAnswers (77M)",
                "PAQ Q&A (64M)",
                "StackExchange (68M)",
                "MS MARCO (9M)",
                "and 24 more datasets"
            ]
        },
        "use_cases": [
            "Semantic search",
            "Text similarity",
            "Clustering",
            "Information retrieval",
            "Duplicate detection",
            "Feature extraction"
        ],
        "performance": {
            "speed": "~1000 sentences/sec on CPU",
            "quality": "High semantic understanding",
            "domain": "General purpose (not domain-specific)"
        }
    }


@app.post("/api/v1/similarity", tags=["Utilities"])
async def compute_similarity(text1: str, text2: str):
    """
    Quick utility to compute similarity between two texts
    Returns cosine similarity score (0-1)
    """
    if not model:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        embeddings = model.encode([text1, text2], normalize_embeddings=True)
        
        # Cosine similarity (dot product when normalized)
        similarity = float(embeddings[0] @ embeddings[1])
        
        return {
            "text1": text1[:100] + "..." if len(text1) > 100 else text1,
            "text2": text2[:100] + "..." if len(text2) > 100 else text2,
            "similarity": round(similarity, 4),
            "interpretation": (
                "Very similar" if similarity > 0.8 else
                "Similar" if similarity > 0.6 else
                "Somewhat similar" if similarity > 0.4 else
                "Not very similar"
            )
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Similarity computation failed: {str(e)}")


# ============================================================================
# Run Instructions
# ============================================================================
# Production: uvicorn app_embedding_service:app --host 0.0.0.0 --port 8000 --workers 2
# Development: uvicorn app_embedding_service:app --reload --host 0.0.0.0 --port 8000
# Docker: uvicorn app_embedding_service:app --host 0.0.0.0 --port 8000
# ============================================================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
