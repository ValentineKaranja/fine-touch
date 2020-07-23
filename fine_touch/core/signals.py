from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import User
from django.contrib.auth import user_logged_in, user_logged_out
# from django.contrib.auth.models import Group
from django.dispatch import receiver

from .models import Customer, LoggedInUser


#  @receiver(pre_save, sender=User)
def customer_profile(sender, instance, created, **kwargs):  # responsible for creating a new profile
    if created:
        # group = Group.objects.get(name='customer')
        # instance.groups.add(group)

        Customer.objects.create(
            user=instance,
            name=instance.username,
            email=instance.email,
        )
        print('profile created')


post_save.connect(customer_profile, sender=User)


@receiver(user_logged_in)
def on_user_logged_in(sender, **kwargs):
    LoggedInUser.objects.get_or_create(user=kwargs.get('user'))



@receiver(user_logged_out)
def on_user_logged_out(sender, **kwargs):
    LoggedInUser.objects.filter(user=kwargs.get('user')).delete()