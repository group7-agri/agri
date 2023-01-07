from django.contrib import admin

# Register your models here.
from .models import Product, Review, Payment, SingleProduct

admin.site.register(Product)
admin.site.register(Review)
admin.site.register(Payment)
admin.site.register(SingleProduct)
