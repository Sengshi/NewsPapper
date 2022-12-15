from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django_apscheduler.models import DjangoJobExecution

from .models import Category, Post, UserCategory


def sender_subs():
    for category in Category.objects.all():
        posts = Post.objects.filter(category=category)
        for user in UserCategory.objects.filter(category=category).values("user"):
            subscriber = User.objects.get(id=user["user"])
            recipient = [subscriber.email]
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
