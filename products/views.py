from django.core import paginator
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Payment
from .forms import ProductForm, ReviewForm
from .utils import searchProducts, paginateProducts
from django import template
from django.utils.timesince import timesince

def products(request):
    products, search_query = searchProducts(request)
    custom_range, products = paginateProducts(request, products, 6)

    context = {'products': products,
               'search_query': search_query, 'custom_range': custom_range}
    return render(request, 'products/products.html', context)

def viewProduct(request, pk):
    products = Product.objects.filter(title=pk)
    custom_range, products = paginateProducts(request, products, 6)

    context = {'products': products, 'title':pk, 'custom_range': custom_range}
    return render(request, 'products/view-product.html', context)

def checkOutProduct(request, pk):
    product = Product.objects.get(id=pk)
    context = {'product': product}
    return render(request, 'products/checkout.html', context)


def product(request, pk):
    productObj = Product.objects.get(id=pk)
    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.product = productObj
        review.owner = request.user.profile
        review.save()

        productObj.getVoteCount

        messages.success(request, 'Your review was successfully submitted!')
        return redirect('product', pk=productObj.id)

    return render(request, 'products/single-product.html', {'product': productObj, 'form': form})


@login_required(login_url="login")
def createProduct(request):
    profile = request.user.profile
    form = ProductForm()

    if request.method == 'POST':
        newpayments = request.POST.get('newpayments').replace(',',  " ").split()
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.owner = profile
            product.save()
            form.save_m2m()

            for payment in newpayments:
                payment, created = Payment.objects.get_or_create(name=payment)
                product.payments.add(payment)
            messages.success(request, 'Successfully')
            return redirect('account')

    context = {'form': form}
    return render(request, "products/product_form.html", context)


@login_required(login_url="login")
def updateProduct(request, pk):
    profile = request.user.profile
    product = profile.product_set.get(id=pk)
    form = ProductForm(instance=product)

    if request.method == 'POST':
        newpayments = request.POST.get('newpayments').replace(',',  " ").split()

        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save()
            for payment in newpayments:
                payment, created = Payment.objects.get_or_create(name=payment)
                product.payments.add(payment)

            return redirect('account')

    context = {'form': form, 'product': product}
    return render(request, "products/product_form.html", context)


@login_required(login_url="login")
def deleteProduct(request, pk):
    profile = request.user.profile
    product = profile.product_set.get(id=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('products')
    context = {'object': product}
    return render(request, 'delete_template.html', context)



register = template.Library()

@register.filter
def naturaltime(value):
    return timesince(value)