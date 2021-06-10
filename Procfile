web: gunicorn Metrica_project.wsgi
worker_1: celery -A Metrica_project worker -l INFO
worker_2: celery -A Metrica_project beat
