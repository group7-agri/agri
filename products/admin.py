from django.contrib import admin
from rangefilter.filters import DateRangeFilter, DateTimeRangeFilter

# Register your models here.
from .models import *


class ProductAdmin(admin.ModelAdmin):
    # list_filter = ('created',DateRangeFilter)
    list_filter = (
        ('created', DateRangeFilter),
    )

    # # If you would like to add a default range filter
    # # method pattern "get_rangefilter_{field_name}_default"
    # def get_rangefilter_created_at_default(self, request):
    #     return (datetime.date.today, datetime.date.today)

    # # If you would like to change a title range filter
    # # method pattern "get_rangefilter_{field_name}_title"
    # def get_rangefilter_created_at_title(self, request, field_path):
    #     return 'custom title'


    search_fields = ('name__name','owner__name', 'quantity', 'location', 'instock', 'created')
    ordering = ('owner', 'name', 'quantity', 'location', 'instock', 'created')
    list_display = ('owner', 'name', 'quantity', 'location', 'instock', 'created')

admin.site.register(Product, ProductAdmin)

class ReviewAdmin(admin.ModelAdmin):
    search_fields = ( 'owner__name','value', 'created')
    ordering = ('owner', 'product', 'value', 'created')
    list_display = ('owner', 'product', 'value', 'created')

admin.site.register(Review, ReviewAdmin)

# class PaymentInline(admin.TabularInline):
#     model = Payment


class PaymentAdmin(admin.ModelAdmin):
    search_fields = ('name', 'created')
    ordering = ('name', 'created')
    list_display = ('name', 'created')
    # inlines = [PaymentInline]



admin.site.register(Payment, PaymentAdmin)



class SingleProductAdmin(admin.ModelAdmin):
    list_filter = ('price',)
    search_fields = ('name', 'price', 'unity')
    ordering = ('name', 'price', 'unity')
    list_display = ('name', 'price', 'unity')

admin.site.register(SingleProduct, SingleProductAdmin)




class OrderAdmin(admin.ModelAdmin):
    list_filter = ('created','quantity')
    
    search_fields = ('id','seller__name','buyer__name', 'price', 'status', 'quantity', 'location', 'created')
    ordering = ('seller', 'buyer', 'productName', 'price', 'status', 'quantity', 'location', 'created')
    list_display = ('seller', 'buyer', 'productName', 'price', 'status', 'quantity', 'location', 'created', 'ProductId')
    
    
    # def has_change_permission(self, request, obj=None):
    #     return False

    # def has_add_permission(self, request, obj=None):
    #     return False

    # def has_view_permission(self, request, obj=None):
    #     return True

admin.site.register(Order, OrderAdmin)
# admin.site.register(Order)


