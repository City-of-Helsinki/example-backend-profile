from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import User, UserData


@receiver(post_save, sender=User)
def create_user_data(sender, instance, created, **kwargs):
    """Creates a UserData instance for the user being created"""
    if created:
        UserData.objects.create(user=instance)
