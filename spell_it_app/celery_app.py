import os
import time

from celery import Celery
from django.conf import settings
import torch

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spell_it_app.settings')

app = Celery('spell_it_app')
app.config_from_object('django.conf:settings')
app.conf.broker_url = settings.CELERY_BROKER_URL
app.autodiscover_tasks()


@app.task()
def debug_task():
    time.sleep(10)
    print('Hello form debug_task')

@app.task()
def debug_torch_task():
    time.sleep(10)

    print('Cuda availability: ', torch.cuda.is_available())