from django.contrib import admin

# Register your models here.

from .models import Profile, Training, Message, Inquiry

admin.site.register(Profile)
admin.site.register(Training)
admin.site.register(Message)
admin.site.register(Inquiry)
