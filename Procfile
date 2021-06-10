web: gunicorn Metrica_project.wsgi
worker: celery -A Metrica_project worker -l INFO
beat: celery -A Metrica_project beat
