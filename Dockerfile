# Dockerfile
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y curl build-essential libpq-dev \
    && apt-get clean

# Install Poetry
ENV POETRY_VERSION=1.8.2
RUN curl -sSL https://install.python-poetry.org | python3 - \
    && ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Copy only poetry files first for caching
COPY pyproject.toml poetry.lock* /app/

# Configure Poetry to not create a virtual environment
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Copy rest of the code
COPY . /app/

# Run migrations and collect static files (can be customized in entrypoint)
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
