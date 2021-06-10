web: gunicorn Metrica_project.wsgi
worker: celery -A Metrica_project worker -l INFO
worker: celery -A Metrica_project beat
