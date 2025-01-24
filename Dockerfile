FROM python:3.13-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && apt-get clean

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Ensure Poetry is in the PATH
ENV PATH="/root/.local/bin:$PATH"  

# Set the working directory
WORKDIR /app

# Copy Poetry files (pyproject.toml and poetry.lock)
COPY pyproject.toml poetry.lock ./

# Install project dependencies (including dev dependencies)
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root --with dev

# Copy the application source code
COPY ./app ./app

# Command to start the service
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]