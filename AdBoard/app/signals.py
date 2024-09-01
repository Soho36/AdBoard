from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from .models import Comment
from django.core.mail import send_mail
from django.conf import settings


@receiver(post_save, sender=User)
def add_user_to_group(sender, instance, created, **kwargs):
    if created:
        group_name = 'Registered'   # Group created in admin panel
        group, created = Group.objects.get_or_create(name=group_name)
        instance.groups.add(group)


@receiver(post_save, sender=Comment)
def notify_post_owner(sender, instance, created, **kwargs):
    if created:
        post = instance.post
        author_email = post.author.email  # Assuming `author` is a User object with an email field
        comment_author = instance.author.username
        comment_content = instance.content

        # Construct the email content
        subject = f"New comment on your post '{post.name}'"
        message = f"""
                Hi {post.author.username},

                {comment_author} has commented on your post "{post.name}":
        
                "{comment_content}"

                View the comment on the site: {settings.SITE_URL}/posts/{post.id}

                Regards,
                Your Site Team
                """

        # Send the email
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,  # Your site's email
            [author_email],  # Recipient list
            fail_silently=False,
        )
