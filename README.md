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

## Project structure

- `manage.py` — Django management script
- `todo_project/` — project settings and URLs
- `todos/` — app with models, views, forms, admin and URLs
- `templates/` — HTML templates
- `requirements.txt` — Python dependencies

## Notes

- Uses SQLite by default (file `db.sqlite3` in project root).
- Date/time inputs use the browser's `datetime-local` control; Django will store them in UTC when `USE_TZ=True` (default in this project).