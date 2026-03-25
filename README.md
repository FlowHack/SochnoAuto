# SochnoAuto

![master](https://github.com/FlowHack/SochnoAuto/actions/workflows/master.yml/badge.svg?branch=master)
![release](https://github.com/FlowHack/SochnoAuto/actions/workflows/release.yml/badge.svg?branch=release)
![SSL](https://img.shields.io/badge/SSL-LetsEncrypt-003545?style=flat&logo=letsencrypt)

![Django](https://img.shields.io/badge/Django-6.0.2-092E20?style=flat&logo=django)
![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat&logo=python)
![License](https://img.shields.io/badge/License-MIT-green)
![Docker](https://img.shields.io/badge/Docker-ready-2496ED?style=flat&logo=docker)
[![Website Status](https://img.shields.io/website?url=https%3A%2F%2Fsochno-auto.ru%2F&label=sochno-auto.ru&logo=ubuntu&style=flat)](https://sochno-auto.ru/)

SochnoAuto — современный сайт автосалона на Django с каталогом автомобилей, умным поиском, формами обратной связи и REST API.

Официальный сайт: **[sochno-auto.ru](https://sochno-auto.ru/)**

> Запустите контейнеры или локальное окружение, выполните миграции и создайте суперпользователя — получите готовый автосалон с формами заявок, отчётами Автотека и API.

## Основные возможности

- **Каталог автомобилей** — просмотр машин по категориям с детальными карточками
- **Умный поиск** — поиск по бренду, модели, году выпуска и другим полям (серверный фильтр + пагинация)
- **Формы заявок** — несколько типов запросов: общая связь, по конкретному авто и запрос отчёта **Автотека**
- **Email‑уведомления** — подтверждение email клиента, уведомления менеджерам, отправка отчёта Автотека
- **REST API** — эндпоинты для категорий, спецпредложений, отзывов и поиска автомобилей
- **Админ‑панель** — сортируемые списки и rich‑text редактор описаний на базе CKEditor 5
- **Адаптивный интерфейс** — верстка на Bootstrap 5, корректно работающая на мобильных устройствах

## Технологический стек

| Категория | Технологии |
|----------|------------|
| Backend | Django 6.0.2, Django REST Framework |
| База данных | PostgreSQL (Docker), SQLite (локальная разработка) |
| Frontend | Vanilla JavaScript, Bootstrap 5 |
| Админка | django-admin-sortable2, CKEditor 5 |
| Сервер | Gunicorn, Nginx |
| Деплой | Docker, Docker Compose |

### API документация

Полная документация API доступна по адресу `/api/swagger/` (Swagger UI) или `/api/redoc/` (ReDoc).

## Структура проекта

```
SochnoAutoRelease/
├── api/                  # REST API endpoints
├── cars/                 # Каталог автомобилей (models, views, services)
├── contacts/             # Формы обратной связи
├── core/                 # Утилиты и контекстные процессоры
├── homepage/             # Главная страница
├── config/               # Настройки Django, URLs, WSGI/ASGI
├── templates/            # HTML шаблоны
├── static/               # CSS, JavaScript, шрифты
├── media/               # Загруженные пользователями файлы
├── nginx/               # Конфигурация Nginx
├── dumps/                # Дампы базы данных
├── Dockerfile            # Определение контейнера
├── docker-compose.yaml   # Оркестрация Docker
├── entrypoint.sh        # Скрипт запуска контейнера
├── manage.py           # Django management
├── manage_dump.py      # Скрипт создания дампов БД
├── .env                 # Переменные окружения
├── requirements.txt     # Зависимости Python
└── fixtures.tar.gz      # Тестовые данные для загрузки в БД
```

## Быстрый старт

### Вариант 1. Docker Compose (приближён к production)

```bash
# Создать папки для статики, медиа и дампов
mkdir -p staticfiles media dumps

# Запустить контейнеры
docker-compose up -d

# Применить миграции и собрать статику
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py collectstatic --noinput

# View logs
docker-compose logs -f

# Application available at http://localhost
```

### Вариант 2. Локальная разработка (без Docker)

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

### Тестовые данные

В проекте есть готовый набор тестовых данных в файле `fixtures.tar.gz`. Для загрузки:

```bash
# Локальный запуск
python manage.py diskette_load fixtures.tar.gz --keep

# В Docker (только данные, без картинок)
docker-compose exec web python manage.py diskette_load fixtures.tar.gz --keep --no-storages
```

> **Примечание:** При использовании Docker с примонтированной папкой `media` может возникнуть ошибка `Device or resource busy`. В этом случае:

```bash
# Скопировать архив из контейнера на хост
docker cp <container_name>:/code/fixtures.tar.gz ./

# Распаковать и загрузить данные
tar -xzf fixtures.tar.gz
docker-compose exec web python manage.py diskette_load fixtures.tar.gz --keep --no-storages

# Удалить временные файлы
rm -rf fixtures.tar.gz
```

После загрузки в базе появятся:
- Категории автомобилей
- Тестовые автомобили с изображениями
- Отзывы
- Изображения для главной страницы

## Тесты

В проекте есть модульные и интеграционные тесты для моделей, форм, сервисов, представлений и API.

### Запуск тестов локально

```bash
# В папке с проектом
source venv/bin/activate
python manage.py test --verbosity=2
```

Покрытие тестами:

- `cars` — модели автомобилей и категорий, валидация, сервисы (`CarService`, `CategoryService`), представления;
- `contacts` — модель заявок, форма `RequestContactForm`, сервис `ContactService`, отправка писем (через mock);
- `homepage` — главная страница, `IndexService`, пагинация (`PaginationMixin`), контекстный процессор текущего года;
- `api` — эндпоинты категорий, поиска, отзывов и специальных предложений.

## Сервисы Docker Compose

| Сервис | Образ | Описание | Порт |
|--------|-------|----------|------|
| `web`  | flowhack/sochno-auto:latest | Django + Gunicorn | 8000 (внутренний)  |
| `db`   | postgres:12.4              | PostgreSQL         | 5432 (внутренний)  |
| `nginx`| nginx:1.19.3               | Reverse proxy      | 80 (внешний)       |

### Управление контейнерами

```bash
# Запуск сервисов
docker-compose up -d

# Остановка сервисов
docker-compose down

# Перезапуск отдельного сервиса
docker-compose restart web

# Просмотр логов
docker-compose logs -f web

# Доступ в shell контейнера
docker-compose exec web bash

# Сбор статики после деплоя
docker-compose exec web python manage.py collectstatic --noinput
```

### Управление базой данных

```bash
# Применить миграции
docker-compose exec web python manage.py migrate

# Создать миграции
docker-compose exec web python manage.py makemigrations

# Полный сброс БД (УДАЛЯЕТ все данные)
docker-compose down
docker-compose up -d
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py collectstatic --noinput
```

## Работа с дампами базы данных

Проект использует библиотеку `diskette` для экспорта и импорта данных.

### Экспорт данных (создание дампа)

```bash
# Локальный запуск (дампит в папку dumps/)
python manage_dump.py

# В Docker (дампит в папку dumps/ на хосте)
docker-compose exec web python manage_dump.py

# С указанием имени файла
python manage_dump.py --filename my_backup
# Результат: dumps/my_backup.tar.gz
```

По умолчанию создаёт файл `dump_15-03-2026_12-30-857.tar.gz`
(формат: `dump_день-месяц-год_час-минута-миллисекунда.tar.gz`).

### Импорт данных (загрузка дампа)

```bash
# Локальный запуск
python manage.py diskette_load путь_к_дампу.gz --keep

# В Docker
docker-compose exec web python manage.py diskette_load путь_к_дампу.gz --keep
```

Ключ `--keep` сохраняет существующие данные в базе. Без него все данные будут удалены перед загрузкой.

### Статические и медиа‑файлы

Nginx обслуживает статику и медиа из папок на хосте (монтируются в контейнер):
- `staticfiles` — статические файлы (CSS, JS), собираются через `collectstatic`;
- `media` — загруженные изображения автомобилей;
- `dumps` — резервные копии базы данных;
- `postgres_data` — файлы базы данных (Docker volume).

## Переменные окружения

Ниже указаны основные переменные, которые нужно прописать в `.env`.  
Значения можно подстроить под вашу инфраструктуру.

### Docker Compose (`.env` рядом с `docker-compose.yaml`)

| Переменная              | Пример значения             | Описание                                                                 |
|-------------------------|-----------------------------|--------------------------------------------------------------------------|
| `DJANGO_SECRET_KEY`     | `your-secret-key`           | Секретный ключ Django (обязателен, хранить в секрете).                  |
| `DJANGO_DEBUG`          | `False`                     | Режим отладки. Для production всегда `False`.                            |
| `DJANGO_ALLOWED_HOSTS`  | `localhost your-domain.com` | Список доменов/хостов, с которых доступно приложение.                    |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | `https://your-domain.com` | Доверенные origin'ы для CSRF (обычно ваш домен с протоколом).     |
| `DJANGO_DB_ENGINE`      | `django.db.backends.postgresql` | Движок базы данных (в Docker по умолчанию PostgreSQL).            |
| `POSTGRES_DB`        | `postgres`                  | Имя базы данных Django.                                                  |
| `POSTGRES_USER`        | `postgres`                  | Пользователь PostgreSQL для подключения Django.                          |
| `POSTGRES_PASSWORD`    | `postgres`                  | Пароль пользователя PostgreSQL для подключения Django.                  |
| `DJANGO_DB_HOST`        | `db`                        | Хост БД внутри docker‑сети (имя сервиса в `docker-compose`).             |
| `DJANGO_DB_PORT`        | `5432`                      | Порт PostgreSQL внутри docker‑сети.                                      |
| `EMAIL_HOST`            | `smtp.yandex.ru`            | SMTP‑сервер для отправки писем.                                          |
| `EMAIL_PORT`            | `465`                       | Порт SMTP (обычно 465 для SSL).                                          |
| `EMAIL_USE_TLS`         | `False`                     | Использовать TLS (обычно `True` при порте 587).                          |
| `EMAIL_USE_SSL`         | `True`                      | Использовать SSL (обычно `True` при порте 465).                          |
| `EMAIL_HOST_USER`       | `your-email@yandex.ru`      | Почта, с которой отправляются письма.                                    |
| `EMAIL_HOST_PASSWORD`   | `your-password`             | Пароль/токен приложения для `EMAIL_HOST_USER`.                           |
| `EMAIL_FOR`             | `admin@example.com`         | Список получателей служебных писем (через пробел).                       |
| `AVITO_SELLER_ID`         | `your-avito-seller-id`        | (Опционально) ID пользователя Avito для интеграции.                      |
| `AVITO_BRAND_ID`         | `your-avito-brand-id`        | (Опционально) ID бренда Avito для интеграции.                      |

### Локальная разработка (`.env` для запуска без Docker)

| Переменная              | Пример значения            | Описание                                                                 |
|-------------------------|----------------------------|--------------------------------------------------------------------------|
| `DJANGO_SECRET_KEY`     | `your-secret-key`          | Секретный ключ Django. Для локалки можно использовать упрощённый.       |
| `DJANGO_DEBUG`          | `True`                     | Включает режим отладки и подробные ошибки.                               |
| `DJANGO_ALLOWED_HOSTS`  | `localhost 127.0.0.1`      | Локальные хосты, с которых можно открыть проект.                         |
| `DJANGO_DB_ENGINE`      | `django.db.backends.sqlite3` | (Опционально) движок БД. По умолчанию SQLite.                          |
| `DJANGO_DB_NAME`        | `db.sqlite3`               | (Опционально) имя файла SQLite.                                          |
| `EMAIL_HOST`            | `smtp.yandex.ru`           | (Опционально) SMTP‑сервер для тестовой отправки писем.                   |
| `EMAIL_PORT`            | `465`                      | Порт SMTP.                                                               |
| `EMAIL_USE_TLS`         | `False`                    | Использовать TLS (для 587).                                             |
| `EMAIL_USE_SSL`         | `True`                     | Использовать SSL (для 465).                                             |
| `EMAIL_HOST_USER`       | `your-email@yandex.ru`     | Почта отправителя. Можно оставить пустой, если не тестируете почту.     |
| `EMAIL_HOST_PASSWORD`   | `your-password`            | Пароль/токен для отправки почты.                                         |
| `EMAIL_FOR`             | `admin@example.com`        | Кому отправлять служебные письма.                                        |
| `AVITO_SELLER_ID`         | `your-avito-seller-id`        | (Опционально) ID пользователя Avito для интеграции.                      |
| `AVITO_BRAND_ID`         | `your-avito-brand-id`        | (Опционально) ID бренда Avito для интеграции.                      |

## Локальная сборка Docker‑образа

Если нужно собрать Docker‑образ самостоятельно вместо использования готового:

```bash
# В docker-compose.yaml:
#   image: flowhack/sochno-auto:latest
# заменить на:
#   build: .

# Затем собрать и запустить
docker-compose up -d --build
```

## SSL и безопасность

Проект использует SSL-сертификат от [Let's Encrypt](https://letsencrypt.org/), который автоматически обновляется.

### Проверка SSL

- [SSL Labs](https://www.ssllabs.com/ssltest/analyze.html?d=sochno-auto.ru) — детальная проверка SSL
- [SSL Checker](https://www.sslshopper.com/ssl-checker.html) — проверка сертификата

## Лицензия

Проект распространяется под лицензией [BSD 3-Clause](LICENSE).
