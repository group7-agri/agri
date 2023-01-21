from django.shortcuts import render
from django.db.models import Sum,Avg,Count,Max,Min
from django.contrib.auth.decorators import login_required
from products.models import *
from users.models import *

@login_required(login_url="login")
def customIndex(request):
    products = Product.objects.all().order_by('created')
    orders = Order.objects.all()
    sumProduct  =  Product.objects.aggregate(Sum('quantity'))
    totalProduct = sumProduct['quantity__sum']

    singleProduct = SingleProduct.objects.all()

   
    confirm = Order.objects.filter(status = 'Confirmed').count()
    confirmrate = (confirm * 100)/ orders.count()

    confirmed = Order.objects.filter (status = 'Confirmed')
    revenue = 0
    for order in confirmed:
        revenue = (order.quantity * order.price) + revenue


    totalestimate = 0
    for single in products:
        sumPrice  =  single.name.price
        totalestimate = (sumPrice * single.quantity) + totalestimate
    
    users = CustomUser.objects.all()
    context = {'products': products, 
                'message': "Am trying",
                'orders' : orders,
                'singleProduct':singleProduct,
                'users': users,
                'revenue': revenue,
                'totalestimate': totalestimate,
                'confirmrate': confirmrate
    }



    return render(request, 'admin/index.html', context)