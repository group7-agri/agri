from django.shortcuts import render

from products.models import Product

def customIndex(request):
    product = Product.objects.all().count()
    context = {'product': product, 
                'message': "Am trying"
    }



    return render(request, 'admin/customs/custom.html', context)