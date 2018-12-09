import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

app = Celery('project')
app.config_from_object('django.conf:settings', namespace="CELERY")

app.autodiscover_tasks()



app.conf.beat_schedule = {
    'change_rating_post': {
        'task': 'project.apps.back_task.tasks.change_rating_post',
        'schedule': 10.0,  # change to `crontab(minute=0, hour=0)` if you want it to run daily at midnight
    },
    'change_rating_thread': {
        'task': 'project.apps.back_task.tasks.change_rating_thread',
        'schedule': 15.0,
    }
}

