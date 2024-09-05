from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from .models import Comment
from django.core.mail import send_mail
from django.conf import settings


@receiver(post_save, sender=User)
def add_user_to_group(sender, instance, created, **kwargs):
    if created:
        group_names = ['Registered', 'Basic']   # Group created in admin panel

        for group_name in group_names:
            group, _ = Group.objects.get_or_create(name=group_name)
            instance.groups.add(group)


@receiver(post_save, sender=Comment)
def notify_post_owner(sender, instance, created, **kwargs):
    """
    Sends an email notification to the post author when post get commented.
    """
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


@receiver(post_save, sender=Comment)
def notify_comment_owner(sender, instance, created, **kwargs):
    """
    Sends an email notification to the comment author when their comment is approved.
    """
    # Only send an email if the comment was just approved (changed from False to True)
    if instance.is_approved and (created or instance.tracker.has_changed('is_approved')):
        send_approval_email(instance)


def send_approval_email(comment):
    """
    Constructs and sends an approval email to the comment author.
    """
    post = comment.post
    author_email = comment.author.email  # Ensure the User model has an email field
    comment_author = comment.author.username
    comment_content = comment.content

    site_url = getattr(settings, 'SITE_URL', 'http://localhost:8000')  # Default to localhost if not set

    subject = f"Your comment to the post '{post.name}' has been approved!"
    message = f"""
Hi {comment_author},

Your comment on the post '{post.name}' has been approved by {post.author.username}:

"{comment_content}"

You can view your comment here: {site_url}/posts/{post.id}/

Regards,
Your Site Team
"""

    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,  # Your site's email
            [author_email],  # Recipient list
            fail_silently=False,
        )
    except Exception as e:
        # Log the error or handle it as needed
        print(f"Error sending email: {e}")
