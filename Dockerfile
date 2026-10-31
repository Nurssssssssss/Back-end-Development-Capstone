FROM python:3.12-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . ./
RUN python manage.py collectstatic --noinput
RUN mkdir -p /app/data && chgrp -R 0 /app/data && chmod -R g=u /app/data
ENV DJANGO_DB_PATH=/app/data/db.sqlite3
USER 1001:0
EXPOSE 8000
CMD ["sh", "-c", "python manage.py migrate --noinput && if [ \"$SEED_DEMO\" = \"1\" ]; then python manage.py seed_demo; fi && exec gunicorn config.wsgi:application --bind 0.0.0.0:8000"]
