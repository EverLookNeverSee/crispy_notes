from celery import shared_task
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.sites.models import Site
from django.conf import settings
from .models import Post
from django.contrib.auth.views import get_user_model

User = get_user_model()


@shared_task
def send_newsletter_email():
    users = User.objects.filter(is_verified=True)
    latest_posts = Post.objects.filter(ok_to_publish=True)[:5]
    body = render_to_string(
        template_name="email/newsletter.html",
        context={"site": Site.objects.get(id=settings.SITE_ID), "posts": latest_posts},
    )
    email_obj = EmailMessage(
        subject="Crispy Notes NewsLetter",
        body=body,
        from_email="newsletter@crispy_notes.com",
        to=[user.email for user in users],
    )
    email_obj.send()
