# celery worker 등록
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE','config.settings')
app=Celery('config')

app.config_from_object('django.conf:settings', namespace='CELERY')

# 장고 config에 등록된 모든 task 모듈을 로드
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')