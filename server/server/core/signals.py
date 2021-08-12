from django.apps import apps
from django.db import DEFAULT_DB_ALIAS


def create_periodic_tasks(
    app_config,
    verbosity=2,
    interactive=True,
    using=DEFAULT_DB_ALIAS,
    apps=apps,
    **kwargs
):
    """
    Create default periodic tasks and store in the database.
    """
    CrontabSchedule = apps.get_model("django_celery_beat.CrontabSchedule")
    PeriodicTask = apps.get_model("django_celery_beat.PeriodicTask")

    every_15_minutes, _ = CrontabSchedule.objects.get_or_create(
        minute="15", hour="*", day_of_week="*", day_of_month="*", month_of_year="*"
    )

    tasks = [
        {
            "name": "Moving average strategy",
            "task": "server.core.tasks.run_strategies_for_users",
            "crontab": every_15_minutes,
        },
    ]

    for task in tasks:
        periodic_task = PeriodicTask.objects.filter(name=task["name"])
        if not periodic_task.exists():
            PeriodicTask.objects.create(**task, enabled=False)
