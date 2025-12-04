"""
FastAPI entry point for image processing backend.
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
import yaml

from src.core.limiter import limiter
from src.api.vectorize import router as vectorize_router
from src.api.rasterize import router as rasterize_router
from src.api.remove_bg import router as remove_bg_router

app = FastAPI(
    title="EK Tools Image Backend",
    description="Image processing API: vectorize, rasterize, and background removal",
    version="0.1.0",
)

# Set up rate limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS middleware
# Only allow from *.eklab.xyz and localhost
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000",
    "http://127.0.0.1",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8000",
]

allow_origin_regex = r"https?://.*\.eklab\.xyz"

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=allow_origin_regex,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(vectorize_router, prefix="/vectorize", tags=["vectorize"])
app.include_router(rasterize_router, prefix="/rasterize", tags=["rasterize"])
app.include_router(remove_bg_router, prefix="/remove-background", tags=["remove-background"])


@app.get("/")
@limiter.limit("100/minute")
async def root(request: Request):
    """Health check endpoint."""
    return {"status": "ok", "message": "EK Tools Image Backend API"}


@app.get("/health")
@limiter.limit("100/minute")
async def health(request: Request):
    """Health check endpoint."""
    return {"status": "healthy"}

@app.on_event("startup")
async def generate_openapi():
    """Generate OpenAPI specification file on startup."""
    openapi_schema = app.openapi()
    with open("openapi.yaml", "w") as f:
        yaml.dump(openapi_schema, f, sort_keys=False)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
