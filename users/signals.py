"""
This module contains signal receivers that are responsible for creating and updating
user profiles in sync with the creation and modification of User model instances.
"""
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """
    Creates a new Profile instance for a newly created User instance.

    This receiver is triggered when a User object is saved for the first time
    (i.e., when created=True). It ensures that each User has a corresponding
    Profile automatically generated upon user creation.
    """
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, created, **kwargs):
    """
    Saves the associated Profile instance when a User instance is saved.

    This receiver is invoked whenever a User object is saved, regardless of
    whether it's a new or existing instance. It guarantees that the Profile
    associated with the User is also updated in the database, maintaining
    consistency between the two models.
    """
    instance.profile.save()


