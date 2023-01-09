from django.contrib import admin

# Register your models here.

from .models import Profile, Training, Message, Inquiry

admin.site.register(Profile)
admin.site.register(Training)


class MessageAdmin(admin.ModelAdmin):
    def has_change_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        return True


# admin.site.register(Message, MessageAdmin)

class InquiryAdmin(admin.ModelAdmin):
    def has_change_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        return True

# admin.site.register(Inquiry, InquiryAdmin)

admin.site.register(Message)
admin.site.register(Inquiry)
