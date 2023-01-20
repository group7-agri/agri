from django.shortcuts import render
from django.db.models import Sum,Avg,Count,Max,Min

from products.models import *
from users.models import *

def customIndex(request):
    products = Product.objects.all().order_by('created')
    orders = Order.objects.all()
    totalProduct  =  Product.objects.aggregate(Sum('quantity'))

    
    users = CustomUser.objects.all()
    context = {'products': products, 
                'message': "Am trying",
                'orders' : orders,
                'users': users,
                'totalProduct': totalProduct['quantity__sum']
    }



    return render(request, 'admin/index.html', context)