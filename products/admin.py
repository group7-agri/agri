from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Product)
admin.site.register(Review)
admin.site.register(Payment)
admin.site.register(SingleProduct)
admin.site.register(Orders)
