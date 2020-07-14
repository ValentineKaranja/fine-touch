from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import User
# from django.contrib.auth.models import Group
from django.dispatch import receiver

from .models import Customer


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