# yourapp/utils.py
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.conf import settings


def send_newsletter(subject, content):
    # Get all subscribed users
    recipients = User.objects.filter(subscription=True).values_list('email', flat=True)

    # Send the email
    send_mail(
        subject,
        content,
        settings.DEFAULT_FROM_EMAIL,
        recipients,
        fail_silently=False,
    )
