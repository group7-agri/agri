from django.contrib import admin

# Register your models here.
from .models import *


class ProductAdmin(admin.ModelAdmin):
    list_display = ('owner', 'name', 'quantity', 'location', 'instock', 'created')

admin.site.register(Product, ProductAdmin)

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('owner', 'product', 'value', 'created')

admin.site.register(Review, ReviewAdmin)

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('name', 'created')

admin.site.register(Payment, PaymentAdmin)

class SingleProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'unity')

admin.site.register(SingleProduct, SingleProductAdmin)




class OrderAdmin(admin.ModelAdmin):
    list_display = ('seller', 'buyer', 'productName', 'price', 'status', 'quantity', 'location', 'created')
    
    
    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        return True

admin.site.register(Order, OrderAdmin)


