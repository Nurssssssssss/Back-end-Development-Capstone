# Back-end-Development-Capstone

Django music/concert site for IBM Python Backend capstone. Four pages: Home, Songs (with accessible modal), Photos/Pictures, Concerts; Django admin at `/admin/`.

## Local setup

```bash
python -m pip install -r requirements.txt
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py migrate
python manage.py seed_demo
python manage.py collectstatic --noinput
python manage.py test
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000. The initial migration files are committed in `catalog`, `songs`, and `photos`, so running `migrate` creates the requested tables.

Optional microservice URLs (otherwise local Django tables are used):

```
SONGS_API_URL=http://127.0.0.1:5002
PICTURES_API_URL=http://127.0.0.1:5001
```

Set `DJANGO_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS` and `DJANGO_DEBUG=0` for cloud deployment. A real user account requires `createsuperuser`; do not include passwords in screenshots or Git history.

**Important:** Kubernetes containers use SQLite by default, which is not suitable for multi-replica production: configure a persistent external database for real production deployments.
