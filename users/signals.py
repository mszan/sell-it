from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.contrib.auth.models import User
from users.models import UserProfile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """
    If user instance is created (user is registered), create related user' profile.
    :param sender: User model
    :param instance: User instance
    """
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, created, **kwargs):
    """
    Save user's profile on user's save.
    :param sender: User model
    :param instance: User instance
    """
    instance.userprofile.save()


@receiver(user_logged_in)
def got_online(sender, user, request, **kwargs):
    """
    Set user's is_online to True.
    """
    user.userprofile.is_online = True
    user.userprofile.save()


@receiver(user_logged_out)
def got_offline(sender, user, request, **kwargs):
    """
    Set user's is_online to False.
    """
    user.userprofile.is_online = False
    user.userprofile.save()
