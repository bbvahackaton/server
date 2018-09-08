"""
Información en:
http://docs.celeryproject.org/en/latest/django/first-steps-with-django.html
"""
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.apps import apps

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
app = Celery('server')
#should have a CELERY_ prefix.
app.config_from_object('django.conf:settings')

#Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: [n.name for n in apps.get_app_configs()])

@app.task(bind=True)
def debug_task(self):
    print("Request: {0!r}".format(self.request))


