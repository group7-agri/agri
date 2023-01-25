from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from django.conf import settings
from .models import Profile
from django.contrib.auth.models import Permission, Group
from django.core.mail import send_mail
from django.conf import settings
from .models import *
import requests

# @receiver(post_save, sender=Profile)
User = settings.AUTH_USER_MODEL

# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def assign_user_permissions(sender, instance, created, **kwargs):
#     if created:
#         user = instance
#         if user.role=='Agronome':
#             user.is_staff = True
#             view_permission = Permission.objects.get(codename='view_secret_data')
#             for project in Project.objects.all():
#                 instance.user_permissions.add(view_permission)



def createProfile(sender, instance, created, **kwargs):
    
    user = instance
    if created == True:
        if user.role=='Normal':
            profile = Profile.objects.create(
                user=user,
                username=user.username,
                email=user.email,
                account=user.status,
                name=user.first_name,
                phone1=user.phone,
            )

            # subject = 'Welcome to YieldSearch'
            # message = 'Hello {} We are glad you are here!'.format(user.first_name)

            # send_mail(
            #     subject,
            #     message,
            #     settings.EMAIL_HOST_USER,
            #     [profile.email],
            #     fail_silently=False,
            # )

            data={
                    'recipients':'{}'.format(user.phone),
                    'message':'Dear {} Thank you for registration keep up with us through \n visit :\n http://192.168.43.119:8000/ or https://agri-portal.up.railway.app/ '.format(user.first_name),
                    'sender':'+250786344674'
                }

            r=requests.post(
                'https://www.intouchsms.co.rw/api/sendsms/.json',
                data,
                auth=('ared123','Ared123?')
                )
            print (r.json(), r.status_code)

        elif user.role=='Admin':
            user.is_staff = True
            user.is_superuser= True
            user.save()

        elif user.role=='Agronome':
            group = Group.objects.get(pk=1)
            user.is_staff = True
            user.groups.add(group)

            
            user.save()
        else:
            pass

    # if created == False:
    #     if user.role=='Admin':
    #         user.is_staff = True
    #         user.is_superuser= True
    #         user.save()
    

    #     elif user.role=='Normal':
    #         user.is_staff = False
    #         user.is_superuser= False
    #         user.save()
            
    #     elif user.role=='Agronome':
    #         group = Group.objects.get(pk=1)
    #         user.is_staff = True
    #         user.groups.add(group)
    #         user.save()
            
    #     else:
    #         pass

    # else:
    #     pass



def updateUser(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user
    if user:
        if created == False:
            user.first_name = profile.name
            user.username = profile.username
            user.email = profile.email
            user.status = profile.account
            user.phone = profile.phone1
            user.save()
    else:
        pass


# def updateRole(sender, instance, created, **kwargs):
#     user =instance
#     if created == False:
#         if user.role=='Admin':
#             user.is_staff = True
#             user.is_superuser= True
#             user.save()
    

#         elif user.role=='Normal':
#             user.is_staff = False
#             user.is_superuser= False
#             user.save()
            
#         elif user.role=='Agronome':
#             group = Group.objects.get(pk=1)
#             user.is_staff = True
#             user.groups.add(group)
#             user.save()
            
#         else:
#             pass

#     else:
#         pass
    
    




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
# post_save.connect(updateRole, sender=settings.AUTH_USER_MODEL)
post_save.connect(updateUser, sender=Profile)
post_delete.connect(deleteUser, sender=Profile)
