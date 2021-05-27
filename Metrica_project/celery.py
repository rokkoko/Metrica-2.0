import os

from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Metrica_project.settings.settings_prod')

app = Celery('Metrica_project')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
