FROM python:3.11-slim

WORKDIR /app

# Install poetry and curl (for healthcheck)
RUN apt-get update && apt-get install -y curl \
    && pip install poetry \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy poetry files
COPY pyproject.toml poetry.lock* ./

# Copy application code
COPY agent/ ./agent/

# Install dependencies and install the package in development mode
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi \
    && pip install -e .

# Expose the port
EXPOSE 8000

# Run the application
CMD ["poetry", "run", "uvicorn", "agent.api:app", "--host", "0.0.0.0", "--port", "8000"] 