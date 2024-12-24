from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from jobprofile.models import Profile

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile(sender, instance, created, **kwargs):
    """
    Automatically creates a Profile for each new user.
    """
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_profile(sender, instance, **kwargs):
    """
    Ensures the Profile is saved when the user is saved.
    """
    if hasattr(instance, 'job_profile'):
        instance.job_profile.save()
