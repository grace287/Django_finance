import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('django_finance')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'analyze-weekly-transactions': {
        'task': 'apps.analysis.tasks.analyze_weekly_transactions',
        'schedule': crontab(hour=0, minute=0, day_of_week='monday'),
    },
    'analyze-monthly-transactions': {
        'task': 'apps.analysis.tasks.analyze_monthly_transactions',
        'schedule': crontab(hour=0, minute=0, day_of_month='1'),
    },
}