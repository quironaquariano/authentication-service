FROM python:3.13-slim

# System dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && apt-get clean

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Make sure poetry is accessible on PATH
ENV PATH="/root/.local/bin:$PATH"  

# Set work directory
WORKDIR /app

# Copy poetry files
COPY pyproject.toml poetry.lock ./

# install all app dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Copy app source code
COPY ./app ./app

# Start the service
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]