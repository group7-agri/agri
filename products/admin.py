from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Product)
admin.site.register(Review)
admin.site.register(Payment)
admin.site.register(SingleProduct)



class OrderAdmin(admin.ModelAdmin):
    def has_change_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        return True

admin.site.register(Order, OrderAdmin)


