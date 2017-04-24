from __future__ import absolute_import
import os
import redis

from celery import Celery
from django.conf import settings
from datetime import timedelta
from django.core.cache import cache

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gifsta.settings')
app = Celery('gifsta')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

app.conf.beat_schedule = {
    'every-minute': {
        'task': 'run_loop',
        'schedule': timedelta(seconds=60), #crontab(minute='*/1'),
    },
    # 'every-minute': {
    #     'task': 'for_run',
    #     'schedule': timedelta(seconds=30), #crontab(minute='*/1'),
    #     'args': [None],
    # }
}

# r = redis.StrictRedis(host='localhost', port=6380, db=0)