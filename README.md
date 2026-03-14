# SochnoAuto

![Django](https://img.shields.io/badge/Django-6.0.2-092E20?style=flat&logo=django)
![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat&logo=python)
![License](https://img.shields.io/badge/License-MIT-green)
![Docker](https://img.shields.io/badge/Docker-ready-2496ED?style=flat&logo=docker)

A modern car dealership website built with Django, featuring a car catalog, search functionality, contact forms, and REST API.

## Features

- **Car Catalog** — Browse vehicles by categories with detailed listings
- **Smart Search** — Find cars by make, model, price, and other criteria
- **Contact Forms** — Multiple form types (general inquiry, specific car, Autoteka service)
- **Email Notifications** — Confirmation emails for contact requests
- **REST API** — Full API for frontend operations
- **Admin Panel** — Sortable lists and rich text editor (CKEditor 5)
- **Responsive Design** — Mobile-friendly with Bootstrap 5

## Tech Stack

| Category | Technology |
|----------|------------|
| Backend | Django 6.0.2, Django REST Framework |
| Database | PostgreSQL (Docker), SQLite (local dev) |
| Frontend | Vanilla JavaScript, Bootstrap 5 |
| Admin | django-admin-sortable2, CKEditor 5 |
| Server | Gunicorn, Nginx |
| Deployment | Docker, Docker Compose |

## Project Structure

```
SochnoAutoRelease/
├── api/              # REST API endpoints
├── cars/             # Car catalog (models, views, services)
├── contacts/         # Contact request forms
├── core/             # Shared utilities & context processors
├── homepage/         # Main page
├── config/           # Django settings, URLs, WSGI/ASGI
├── templates/        # HTML templates
├── static/           # CSS, JavaScript, fonts
├── media/            # User uploads
├── nginx/            # Nginx configuration
├── Dockerfile        # Container definition
├── docker-compose.yaml
├── .env              # Environment variables
└── requirements.txt
```

## Quick Start

### Docker Compose (Production)

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Application available at http://localhost
```

### Local Development

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run migrations (SQLite by default)
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

Application available at http://127.0.0.1:8000

## Docker Compose Services

| Service | Image | Description | Port |
|---------|-------|-------------|------|
| `web` | flowhack/sochno-auto-release:latest | Django + Gunicorn | 8000 (internal) |
| `db` | postgres:12.4 | PostgreSQL | 5432 (internal) |
| `nginx` | nginx:1.19.3 | Reverse proxy | 80 (external) |

### Managing Containers

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# Restart a service
docker-compose restart web

# View logs
docker-compose logs -f web

# Access container shell
docker-compose exec web bash
```

### Database Management

```bash
# Run migrations
docker-compose exec web python manage.py migrate

# Create migrations
docker-compose exec web python manage.py makemigrations

# Reset database (WARNING: deletes all data)
docker-compose down -v
docker-compose up -d
docker-compose exec web python manage.py migrate
```

### Static & Media Files

Nginx serves static/media from Docker volumes:
- `static_value` — Static files (CSS, JS)
- `media_value` — User uploads (car images)
- `postgres_data` — Database files

## Environment Variables

### Docker Compose (.env)

```bash
# Django
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=localhost your-domain.com
DJANGO_CSRF_TRUSTED_ORIGINS=https://your-domain.com

# PostgreSQL
DJANGO_DB_ENGINE=django.db.backends.postgresql
DJANGO_DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=postgres
DB_HOST=db
DB_PORT=5432

# Email
EMAIL_HOST=smtp.yandex.ru
EMAIL_PORT=465
EMAIL_USE_TLS=False
EMAIL_USE_SSL=True
EMAIL_HOST_USER=your-email@yandex.ru
EMAIL_HOST_PASSWORD=your-password
EMAIL_FOR=admin@example.com

# Optional
AVITO_USER_ID=your-avito-user-id
```

### Local Development (.env)

```bash
# Django
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1

# SQLite (default - no additional config needed)
# DJANGO_DB_ENGINE=django.db.backends.sqlite3
# DJANGO_DB_NAME=db.sqlite3

# Email (optional)
EMAIL_HOST=smtp.yandex.ru
EMAIL_PORT=465
EMAIL_USE_TLS=False
EMAIL_USE_SSL=True
EMAIL_HOST_USER=your-email@yandex.ru
EMAIL_HOST_PASSWORD=your-password
EMAIL_FOR=admin@example.com

# Optional
AVITO_USER_ID=your-avito-user-id
```


## Building Docker Image Locally

To build the image locally instead of using the pre-built one:

```bash
# Modify docker-compose.yaml:
# Change: image: flowhack/sochno-auto-release:latest
# To:     build: .

# Then build and start
docker-compose up -d --build
```

## License

[MIT License](LICENSE)
