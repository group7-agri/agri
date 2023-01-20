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
    
    totalestimate = 0
    for single in products:
        sumPrice  =  single.name.price
        totalestimate = (sumPrice * single.quantity) + totalestimate
    
    users = CustomUser.objects.all()
    context = {'products': products, 
                'message': "Am trying",
                'orders' : orders,
                'users': users,
                'totalestimate': totalestimate
    }



    return render(request, 'admin/index.html', context)