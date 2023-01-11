from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm
from django.contrib.auth.models import Group
from django.conf import settings
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

# Register your models here.

from .models import Profile, Training, Message, Inquiry, CustomUser


User = settings.AUTH_USER_MODEL

class MessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created')
    
    search_fields = ('name', 'email', 'created')
    ordering = ('name', 'email', 'created')
    filter_horizontal = ()

    
    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        return True


admin.site.register(Message)
# admin.site.register(Message, MessageAdmin)

class InquiryAdmin(admin.ModelAdmin):
    
    search_fields = ('name', 'email', 'created')
    ordering = ('name', 'email', 'created')
    
    list_display = ('name', 'email', 'created')
    filter_horizontal = ()

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        return True

# admin.site.register(Inquiry, InquiryAdmin)

admin.site.register(Inquiry)



class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone', 'first_name', 'role')



class CustomUserAdmin(UserAdmin):
     # The forms to add and change user instances
    form = UserChangeForm
  
    search_fields = ('first_name', 'email', 'phone', 'username', 'role')
    ordering = ('first_name', 'email', 'phone', 'username', 'role')
    filter_horizontal = ()

    list_display = ('first_name', 'email', 'phone', 'username', 'role')
    add_form = CustomUserCreationForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'email','phone','username', 'password1', 'password2','role'),
        }),
    )

    fieldsets = (
        (None, {'fields': ('first_name', 'email', 'phone', 'username', 'role')}),
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
    search_fields = ('user', 'name', 'email', 'account', 'location')
    ordering = ('user', 'name', 'email', 'account', 'location')
    filter_horizontal = ()
    list_display = ('user', 'name', 'email', 'account', 'location')


admin.site.register(Profile, ProfileAdmin)

#  #Profile, Training, Message, Inquiry, CustomUser
class TrainingAdmin(admin.ModelAdmin):
    search_fields = ('owner', 'trainer', 'completed', 'created')
    ordering = ('owner', 'trainer', 'completed', 'created')
    filter_horizontal = ()
    list_display = ('owner', 'trainer', 'completed', 'created')

admin.site.register(Training, TrainingAdmin)

