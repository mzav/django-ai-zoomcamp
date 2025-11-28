# Django TODO Application

Simple TODO app built with Django. Features:
- Create, edit, and delete TODOs
- Assign due dates (date and time)
- Mark TODOs as resolved/unresolved

## Quick Start

1) Create and activate a virtual environment
```
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2) Install dependencies
```
pip install -r requirements.txt
```

3) Apply migrations
```
python manage.py migrate
```

4) Run the development server
```
python manage.py runserver
```

Open the app at http://127.0.0.1:8000/

## Optional: Admin

Create a superuser to access the Django admin (to manage TODOs there as well):
```
python manage.py createsuperuser
```
Then visit http://127.0.0.1:8000/admin/

## Running tests

Run the Django test suite (uses an isolated in-memory SQLite database by default):
```
python manage.py test
```

## Project structure

- `manage.py` — Django management script
- `todo_project/` — project settings and URLs
- `todos/` — app with models, views, forms, admin and URLs
- `templates/` — HTML templates
- `requirements.txt` — Python dependencies

## Notes

- Uses SQLite by default (file `db.sqlite3` in project root).
- Date/time inputs use the browser's `datetime-local` control; Django will store them in UTC when `USE_TZ=True` (default in this project).

## Docker

Build the image:
```
docker build -t django-ai-zoomcamp:latest .
```

Run the container (exposes port 8000):
```
docker run --rm -p 8000:8000 \
  -e DJANGO_SECRET_KEY="change-me" \
  -v $(pwd)/db.sqlite3:/app/db.sqlite3 \
  django-ai-zoomcamp:latest
```

Open http://127.0.0.1:8000

The container entrypoint will run `python manage.py migrate` before starting Gunicorn.

### GitHub Actions (CI) — Build & Publish

This repo includes a GitHub Actions workflow that builds the Docker image on pushes and PRs. On pushes to `main`/`master` and tags like `v1.2.3`, it publishes the image to GitHub Container Registry (GHCR) under `ghcr.io/<owner>/<repo>`.

No extra secrets are required; it uses `GITHUB_TOKEN` by default. After the first push, you can pull the image like:
```
docker pull ghcr.io/<owner>/<repo>:<tag>
```

If you prefer Docker Hub, replace the registry/login steps in `.github/workflows/docker-image.yml` with your Docker Hub credentials and change the `images:` value in the metadata action accordingly.