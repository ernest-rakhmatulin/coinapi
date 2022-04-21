from django.core.management.base import BaseCommand
from django_celery_beat.models import CrontabSchedule, PeriodicTask


class Command(BaseCommand):
    help = 'Initiates Celery Beat\'s periodic tasks.'

    def handle(self, *args, **options):
        # CrontabSchedule's minute, hour, day_of_week, etc. is equal
        # to '*' by default. We specify minute='0', to run tasks every hour.
        every_hour_cron = CrontabSchedule(minute='0')
        every_hour_cron.save()

        periodic_task = PeriodicTask(
            name='Refresh Currency Exchange Rate',
            task='core.tasks.refresh_currency_exchange_rate_task',
            crontab=every_hour_cron,
        )
        periodic_task.save()

        self.stdout.write(f'Periodic task "{periodic_task.task}" successfully added.')
