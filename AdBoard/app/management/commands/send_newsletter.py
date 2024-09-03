from django.core.management.base import BaseCommand
from app.models import Newsletter
from app.utils import send_newsletter  # Import the function
from django.utils import timezone


class Command(BaseCommand):
    help = 'Send out the latest newsletter to all subscribers'

    def handle(self, *args, **kwargs):
        try:
            newsletter = Newsletter.objects.filter(sent_at__isnull=True).latest('created_at')
            send_newsletter(newsletter.subject, newsletter.content)
            newsletter.sent_at = timezone.now()
            newsletter.save()
            self.stdout.write(self.style.SUCCESS('Successfully sent newsletter'))
        except Newsletter.DoesNotExist:
            self.stdout.write(self.style.WARNING('No unsent newsletters found'))
