import os
from celery import Celery

# Establecer la variable de entorno para configuraciones de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Crear la aplicación Celery
app = Celery('config')

# Namespace para evitar colisiones con otras configuraciones de Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Buscar tareas automáticamente en todas las aplicaciones registradas
app.autodiscover_tasks()

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
