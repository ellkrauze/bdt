from celery.schedules import crontab

CELERYBEAT_SCHEDULE = {
    'run-every-24-hours': {
        'task': 'app.run_image_downloader',
        'schedule': crontab(hour=24, minute=0),
    },
}