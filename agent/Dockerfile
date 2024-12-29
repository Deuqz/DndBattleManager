FROM python:3.11-slim

WORKDIR /app

# Install poetry and curl (for healthcheck)
RUN apt-get update && apt-get install -y curl \
    && pip install poetry==1.7.1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy only necessary files first
COPY pyproject.toml ./
COPY *.py ./

# Install dependencies
RUN poetry config virtualenvs.create false \
    && poetry lock --no-update \
    && poetry install --no-interaction --no-ansi

# Copy remaining application code
COPY . .

# Expose the port
EXPOSE 8077

# Run the application
CMD ["poetry", "run", "uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8077"] 