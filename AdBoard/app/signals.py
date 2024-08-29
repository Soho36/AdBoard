from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group


@receiver(post_save, sender=User)
def add_user_to_group(sender, instance, created, **kwargs):
    if created:
        group_name = 'Registered'   # Group created in admin panel
        group, created = Group.objects.get_or_create(name=group_name)
        instance.groups.add(group)
