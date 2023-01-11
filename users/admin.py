from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm
from django.contrib.auth.models import Group

# Register your models here.

from .models import Profile, Training, Message, Inquiry, CustomUser




class MessageAdmin(admin.ModelAdmin):
    
    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        return True


admin.site.register(Message)
# admin.site.register(Message, MessageAdmin)

class InquiryAdmin(admin.ModelAdmin):
    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        return True

# admin.site.register(Inquiry, InquiryAdmin)

admin.site.register(Inquiry)




class CustomUserAdmin(UserAdmin):
    list_display = ('first_name', 'email', 'phone', 'username', 'role')
    add_form = CustomUserCreationForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'email','phone','username', 'password1', 'password2','role'),
        }),
    )



# class CustomUserChangeForm(UserChangeForm):

#     class Meta(UserChangeForm.Meta):
#         model = CustomUser
#         fields = ('first_name', 'email','phone','username','role')

# class CustomUserAdmin(UserAdmin):
#     form = CustomUserChangeForm

admin.site.register(CustomUser, CustomUserAdmin)


#CUSTOMIZING INTERFACE

admin.site.unregister(Group)
admin.site.site_header =  'Yield Administration'

 #Profile, Training, Message, Inquiry, CustomUser
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'email', 'account', 'location')


admin.site.register(Profile, ProfileAdmin)

#  #Profile, Training, Message, Inquiry, CustomUser
class TrainingAdmin(admin.ModelAdmin):
    list_display = ('owner', 'trainer', 'completed', 'created')

admin.site.register(Training, TrainingAdmin)
