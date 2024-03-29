import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

app = Celery('project')
app.config_from_object('django.conf:settings', namespace="CELERY")

app.autodiscover_tasks()



app.conf.beat_schedule = {
    'del_users_not_active': {
        'task': 'project.apps.back_task.tasks.delete_not_activ_user',
       'schedule': crontab(minute=0, hour=0),  # change to `crontab(minute=0, hour=0)` if you want it to run daily at midnight
    },

}

