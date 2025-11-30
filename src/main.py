"""
FastAPI entry point for image processing backend.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.vectorize import router as vectorize_router
from src.api.rasterize import router as rasterize_router
from src.api.remove_bg import router as remove_bg_router

app = FastAPI(
    title="EK Tools Image Backend",
    description="Image processing API: vectorize, rasterize, and background removal",
    version="0.1.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(vectorize_router, prefix="/vectorize", tags=["vectorize"])
app.include_router(rasterize_router, prefix="/rasterize", tags=["rasterize"])
app.include_router(remove_bg_router, prefix="/remove-background", tags=["remove-background"])


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"status": "ok", "message": "EK Tools Image Backend API"}


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

