from django.apps import apps as global_apps
from django.db import DEFAULT_DB_ALIAS


def create_periodic_tasks(app_config, verbosity=2, interactive=True, using=DEFAULT_DB_ALIAS, apps=global_apps, **kwargs):  # NOQA
    """
    Create default periodic tasks and store in the database.
    """
    CrontabSchedule = apps.get_model('django_celery_beat.CrontabSchedule')
    PeriodicTask = apps.get_model('django_celery_beat.PeriodicTask')

    on_the_minute, _ = CrontabSchedule.objects.get_or_create(
        minute='1',
        hour='*',
        day_of_week='*',
        day_of_month='*',
        month_of_year='*'
    )
    on_30_minute, _ = CrontabSchedule.objects.get_or_create(
        minute='30',
        hour='*',
        day_of_week='*',
        day_of_month='*',
        month_of_year='*'
    )
    on_45_minute, _ = CrontabSchedule.objects.get_or_create(
        minute='45',
        hour='*',
        day_of_week='*',
        day_of_month='*',
        month_of_year='*'
    )
    on_the_hour, _ = CrontabSchedule.objects.get_or_create(
        minute='0',
        hour='*',
        day_of_week='*',
        day_of_month='*',
        month_of_year='*'
    )
    six_hourly, _ = CrontabSchedule.objects.get_or_create(
        minute='0',
        hour='*/6',
        day_of_week='*',
        day_of_month='*',
        month_of_year='*'
    )
    daily, _ = CrontabSchedule.objects.get_or_create(
        minute='0',
        hour='*/24',
        day_of_week='*',
        day_of_month='*',
        month_of_year='*'
    )

    tasks = [
        {
            'name': 'Update Assets',
            'task': 'api.assets.tasks.update_asset_models',
            'crontab': on_the_hour
        },
        # {
        #     'name': 'Event Reminders',
        #     'task': 'api.events.tasks.send_event_reminders',
        #     'crontab': on_the_hour
        # },
        # {
        #     'name': 'Update Group Members',
        #     'task': 'api.customgroups.tasks.update_filter_group_members',
        #     'crontab': on_45_minute
        # },
        # {
        #     'name': 'Update Role Members',
        #     'task': 'api.users.tasks.sync_role_members',
        #     'crontab': on_30_minute
        # },
        # {
        #     'name': 'Update Notice Audience Follows',
        #     'task': 'api.notices.tasks.update_notice_follows',
        #     'crontab': six_hourly
        # },
        # {
        #     'name': 'Update Calendar Feeds',
        #     'task': 'api.calendars.tasks.update_calendar_feeds',
        #     'crontab': six_hourly
        # },
    ]

    for task in tasks:
        periodic_task = PeriodicTask.objects.filter(name=task['name'])
        if not periodic_task.exists():
            PeriodicTask.objects.create(**task)
