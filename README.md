# StudioHub

StudioHub is a lightweight task tracker built with Django. It provides a Kanban-style dashboard for managing client projects.

## Features
- Create clients and tasks
- Drag and drop tasks between statuses
- Automatic tracking of completion dates
- Docker ready and deployable to Render.com

## Quick start
1. Create a virtual environment and install dependencies

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Copy `.env.example` to `.env` and update the values. At minimum set `SECRET_KEY`
   to a random string. If omitted, a random key will be generated automatically
   for development, but you should provide your own in production. You can
   generate one with:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

3. Run migrations and start the development server

```bash
python manage.py migrate
python manage.py runserver
```

Visit `http://localhost:8000` to access the dashboard.

## Running tests
Execute the Django test suite with:

```bash
python manage.py test
```

## Docker
A `Dockerfile` and `docker-compose.yml` are provided for containerized development.

## Deploying to Render

The `render.yaml` blueprint allows you to deploy StudioHub with a single click.

1. Sign in to [Render](https://render.com) and choose **New \> Blueprint**.
2. Enter the repository URL and confirm the services to create.
3. Render will provision a PostgreSQL database, Redis, a web service, and Celery workers.
4. Once the build finishes, open the web service URL to access your hosted instance.


## Troubleshooting
If you encounter a 500 error when accessing the dashboard, ensure the database migrations have run and that the `SECRET_KEY` environment variable is set:

```bash
python manage.py migrate
```

The application requires a valid database schema and secret key to display the dashboard correctly.

