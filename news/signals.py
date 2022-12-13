from django.contrib.auth.models import User
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import UserCategory, Post, PostCategory


@receiver(m2m_changed, sender=Post.category.through)
def notify_subscribers(sender, instance, action, **kwargs):
    if action == 'post_add':
        category = PostCategory.objects.get(post=instance.id).category
        for user in UserCategory.objects.filter(category=category).values("user"):
            subscriber = User.objects.get(id=user["user"])
            recipient = [subscriber.email]
            html_content = render_to_string(
                'news_created.html',
                {
                    'post': instance,
                    'subscriber': subscriber,
                }
            )
            msg = EmailMultiAlternatives(
                subject=f'{instance.title}',
                body=instance.post,
                from_email='testpysend@mail.ru',
                to=recipient,
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()
