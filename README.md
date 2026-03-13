# SochnoAuto

A car dealership website built with Django.

## Tech Stack

- **Backend:** Django 6.0.2, Django REST Framework
- **Database:** SQLite (default), PostgreSQL support via environment variables
- **Admin:** django-admin-sortable2, django-ckeditor-5
- **Frontend:** Vanilla JavaScript, Bootstrap 5

## Features

- Car catalog with categories and detailed listings
- Car search functionality
- Contact request forms (general inquiry, specific car, Autoteka service)
- Email confirmation for contact requests
- Pagination for car listings and feedback
- REST API for frontend operations
- Responsive design

## Project Structure

```
SochnoAutoRelease/
├── api/              # REST API endpoints
├── cars/             # Car catalog (views, services)
├── contacts/         # Contact request forms and management
├── core/             # Shared services and utilities
├── homepage/         # Main page and homepage services
├── config/           # Django settings, URLs, WSGI/ASGI
├── templates/        # Base templates
├── static/           # CSS, JavaScript, fonts
└── media/            # User uploads
```

## Installation

1. Create virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or
   venv\Scripts\activate  # Windows
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create `.env` file:
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

4. Run migrations:
   ```bash
   python manage.py migrate
   ```

5. Create superuser:
   ```bash
   python manage.py createsuperuser
   ```

6. Run development server:
   ```bash
   python manage.py runserver
   ```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DJANGO_SECRET_KEY` | Django secret key | Required |
| `DJANGO_DEBUG` | Debug mode | `True` |
| `DJANGO_ALLOWED_HOSTS` | Allowed hosts | `localhost` |
| `DJANGO_DB_ENGINE` | Database engine | `sqlite3` |
| `DJANGO_DB_NAME` | Database name | `db.sqlite3` |
| `EMAIL_HOST_USER` | SMTP email yandex user | - |
| `EMAIL_HOST_PASSWORD` | SMTP email yandex password | - |

## License

MIT License
