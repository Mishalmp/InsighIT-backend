from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'insight.settings')


app = Celery('insight')


app.conf.enable_utc = False

app.conf.update(timezone = 'Asia/Kolkata')

app.config_from_object(settings, namespace='CELERY')


app.conf.beat_schedule = {

    'send-mail-every-day-at-8':{
        'task':'accounts.tasks.send_mail_func',
        'schedule':crontab(hour=9,minute=0),
        # 'schedule':crontab(),
        # 'args':(2,)
    },
        'check-expiring-subscriptions': {
        'task': 'accounts.tasks.check_expiring_subscription',
        'schedule': crontab(hour=0, minute=0),  # Run daily at midnight
    },

}


app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}") 