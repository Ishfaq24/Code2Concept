"""
FastAPI application factory and router setup.
Main entry point for the backend service.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.generate import router

# Create FastAPI app
app = FastAPI(
    title="Code2Concept - Video Generation API",
    description="Generate educational videos from topics using AI and Manim animations",
    version="1.0.0"
)


# CORS Middleware - Allow frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(router)


@app.get("/")
def root():
    """Root endpoint - API information"""
    return {
        "name": "Code2Concept - Video Generation API",
        "version": "1.0.0",
        "endpoints": {
            "POST /generate": "Generate video from topic",
            "POST /refine": "Refine generated video with feedback",
            "GET /video": "Get the generated video",
            "GET /status": "Get generation status",
            "POST /health": "Health check"
        }
    }


@app.get("/health")
def health():
    """Health check endpoint"""
    return {"status": "healthy"}

