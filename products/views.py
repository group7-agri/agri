from django.core import paginator
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product,Order, Payment, SingleProduct, Review
from .forms import ProductForm, ReviewForm
from .utils import searchProducts, paginateProducts
from django.views.decorators.csrf import csrf_exempt
from django import template
from users.models import Profile
from django.utils.timesince import timesince

def products(request):
    products, search_query = searchProducts(request)
    custom_range, products = paginateProducts(request, products, 6)

    context = {'products': products,
               'search_query': search_query, 'custom_range': custom_range}
    return render(request, 'products/products.html', context)

def viewProduct(request, pk):
    item = SingleProduct.objects.get(name=pk)
    products = Product.objects.filter(name=item)
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



@login_required(login_url="login")
def processOrder(request, pk):


    #DATA 
    buyer = request.user.profile
    seller = Profile.objects.get(id=pk)
    
    productId = ''
    SingleId = ''

    

    if request.method == 'POST':
        productName = request.POST['productName']
        productId = request.POST['productId']
        price = request.POST['price']
        SingleId = request.POST['SingleId']
        unity = request.POST['unity']
        totalQuantity = int(request.POST['TotalQuantity'])
        needQuantity = int(request.POST['quantityNeeded'])

        quantity = totalQuantity - needQuantity
        location = request.POST['location']
        reason = request.POST['reason']


        #CHOICE MADE
        choice = request.POST['choice']


        if quantity >=0:
            order = Order.objects.create(
            seller=seller,
            buyer=buyer,
            productName=productName,
            price=price,
            unity=unity,
            quantity=needQuantity,
            location=location,
            request=reason)

            obj = order.save()
                    # Get the instance of the model that you want to update
            prod = Product.objects.get(id=productId)
            item = SingleProduct.objects.get(id=SingleId)

            # Update the field values of the model instance
            prod.quantity = quantity

            # Save the changes to the database
            prod.save()


            if choice == 'Resell':
                newProd = Product.objects.create(
                    owner=buyer,
                    name=item.id,
                    featured_image = prod.featured_image,
                    description=prod.description,
                    quantity=needQuantity,
                    location=location
                )
                newProd.save()

            
            if obj is None:
                messages.success(request, 'Your order sent successfully!')
                return redirect('products')
            else:
                messages.error(request, 'Error for inserting order')
                return redirect('checkout-product',pk=productId)

        else :
            messages.error(request, 'Quantity can not exceed  {}'.format(totalQuantity))
            return redirect('checkout-product',pk=productId)

    else:
        messages.info(request, 'something went wrong!!')
        return redirect('checkout-product',pk=productId)
     



register = template.Library()

@register.filter
def naturaltime(value):
    return timesince(value)



