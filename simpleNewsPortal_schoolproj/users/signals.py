from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

# user -> sender
# receiver -> receiver
'''we want a user profile to be created for each new user'''


@receiver(signal=post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


# saves our profile every time the User objects gets saved
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
