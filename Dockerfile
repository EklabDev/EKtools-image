# Use an official Python runtime as a parent image
FROM python:3.13-slim-bookworm

# Install system dependencies
# potrace: for vectorization
# libcairo2: for cairosvg
# build-essential: for compiling some python packages if needed
# libgl1: for opencv
RUN apt-get update && apt-get install -y \
    potrace \
    libcairo2 \
    build-essential \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Set work directory
WORKDIR /app

# Copy project files
COPY pyproject.toml .
COPY uv.lock .
COPY README.md .
COPY src/ src/

# Install dependencies
# We use --system to install directly into the system python environment
# since we are already in a container
RUN uv sync --frozen --no-dev

# Expose port
EXPOSE 8000

# Run the application
CMD ["uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]

