import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django.shortcuts import render
from django.template import Context
from django.template.loader import get_template, render_to_string
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from news.models import UserCategory, Category, Post
from requests import request

logger = logging.getLogger(__name__)


def sender_subs():
    for category in Category.objects.all():
        posts = Post.objects.filter(category=category)
        # print(category)
        for user in UserCategory.objects.filter(category=category).values("user"):
            subscriber = User.objects.get(id=user["user"])
            recipient = [subscriber.email]
            # print(recipient)
            html_content = render_to_string(
                'news_subs.html',
                {
                    'posts': posts,
                    'subscriber': subscriber,
                    'category': category,
                },
            )
            msg = EmailMultiAlternatives(
                subject=f'News from week',
                from_email='testpysend@mail.ru',
                to=recipient,
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()

def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")
        scheduler.add_job(
            sender_subs,
            trigger=CronTrigger(second="*/10"),
            id="my_job",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

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
