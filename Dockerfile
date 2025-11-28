FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# System deps (add build tools only if needed for native deps)
RUN groupadd -r app && useradd -r -g app app \
    && apt-get update && apt-get install -y --no-install-recommends \
       build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps first to leverage Docker layer caching
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy project
COPY . /app

# Ensure non-root user owns the application directory for SQLite, migrations, etc.
RUN chown -R app:app /app

# Switch to non-root user
USER app

# Expose port for the web server
EXPOSE 8000

# Default command: run with Gunicorn over WSGI
# DJANGO_SETTINGS_MODULE defaults to todo_project.settings via manage.py, but set explicitly if needed
ENV DJANGO_SETTINGS_MODULE=todo_project.settings

# Collect static is optional; uncomment if you add staticfiles storage
# RUN python manage.py collectstatic --noinput

CMD ["/bin/sh", "-c", "python manage.py migrate --noinput && gunicorn todo_project.wsgi:application --bind 0.0.0.0:8000 --workers 3 --timeout 120"]
