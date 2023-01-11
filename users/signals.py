from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from django.conf import settings

from .models import Profile
from django.contrib.auth.models import Permission
from django.core.mail import send_mail
from django.conf import settings
from .models import *

# @receiver(post_save, sender=Profile)
User = settings.AUTH_USER_MODEL

def createProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        if user.role=='Normal':
            profile = Profile.objects.create(
                user=user,
                username=user.username,
                email=user.email,
                account=user.status,
                name=user.first_name,
            )

            subject = 'Welcome to YieldSearch'
            message = 'Hello {} We are glad you are here!'.format(user.first_name)

            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [profile.email],
                fail_silently=False,
            )
        elif user.role=='Admin':
            user.is_staff = True
            user.is_superuser= True
            user.save()

        elif user.role=='Agronome':
            user.is_staff = True
            # view_permission = Permission.objects.get(codename='view_secret_data')
            # delete_permission = Permission.objects.get(codename='delete_secret_data')
            # instance.user_permissions.add(view_permission, delete_permission)

            
            user.save()
        else:
            pass


def updateUser(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user
    if user:
        if created == False:
            user.first_name = profile.name
            user.username = profile.username
            user.email = profile.email
            user.status = profile.account
            user.save()
    else:
        pass

    


def deleteUser(sender, instance, **kwargs):
    try:
        user = instance.user
        if user:
            user.delete()
        else:
            pass
    except:
        pass




post_save.connect(createProfile, sender=settings.AUTH_USER_MODEL)
post_save.connect(updateUser, sender=Profile)
post_delete.connect(deleteUser, sender=Profile)
