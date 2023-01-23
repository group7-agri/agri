from django.shortcuts import render, redirect
from django.db.models import Sum,Avg,Count,Max,Min
from django.contrib.auth.decorators import login_required
from products.models import *
from users.models import *
from datetime import date, timedelta
from django.http import Http404
from django import template

def custom_404(request, exception):
    return render(request, '404.html', status=404)

@login_required(login_url="login")
def customIndex(request):
    if not request.user.is_staff:
        return redirect('profiles')
    products = Product.objects.all().order_by('-created')

    distint_product = Product.objects.values('name').distinct()
    orders = Order.objects.all()
    sumProduct  =  Product.objects.aggregate(Sum('quantity'))
    totalProduct = sumProduct['quantity__sum']

    # SEASON PRODUCTS
   
    # Get all books created before last 6 months
    end_date1 = date.today() - timedelta(days=3)
    print(end_date1)
    season_a= Product.objects.filter(created__lt=end_date1)

    # Get all books created in the next 6 months
    start_date = date.today()
    end_date = start_date - timedelta(days=1)
    # season_b = Product.objects.filter(created__range=(start_date, end_date))
    season_b = Product.objects.filter(created__gt=end_date1)


    singleProduct = SingleProduct.objects.all()
    
   
    confirm = Order.objects.filter(status = 'Confirmed').count()
    confirmrate = (confirm * 100)/ orders.count()
    confirmrate = "{:.2f}".format(confirmrate)
    confirmed = Order.objects.filter (status = 'Confirmed')
    revenue = 0
    for order in confirmed:
        revenue = (order.quantity * order.price) + revenue


    totalestimate = 0
    for single in products:
        sumPrice  =  single.name.price
        totalestimate = (sumPrice * single.quantity) + totalestimate
    
    users = CustomUser.objects.all().order_by('-date_joined')
    
    distinct_orders= Order.objects.distinct()

    context = {'products': products, 
                'message': "Am trying",
                'orders' : orders,
                'singleProduct':singleProduct,
                'users': users,
                'revenue': revenue,
                'distint_product':distint_product,
                'distinct_orders':distinct_orders,
                'totalestimate': totalestimate,
                'confirmrate': confirmrate,
                'season_b':season_b,
                'season_a':season_a
                
    }



    return render(request, 'admin/index.html', context)


register = template.Library()
@register.filter
def truncate_decimal(value, decimal_places):
    """
    Truncates a float to a given number of decimal places without rounding.
    """
    if not isinstance(value, float):
        return value
    return "%.{}f".format(decimal_places) % value