from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
import logging
from .sheduler_tasks import delete_old_job_executions, sender_subs


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BackgroundScheduler()
        scheduler.add_jobstore(DjangoJobStore(), "default")
        scheduler.add_job(
            sender_subs,
            trigger=CronTrigger(
                day_of_week="sun", hour="23", minute="30"
            ),
            id="sender_subs",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'sender_subs'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
