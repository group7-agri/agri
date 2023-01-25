from django.core import paginator
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product,Order, Payment, SingleProduct, Review
from .forms import ProductForm, ReviewForm, TraderProductForm
from .utils import searchProducts, paginateProducts
from django.views.decorators.csrf import csrf_exempt
from django import template
from django.db.models import Q
from users.models import Profile
from django.utils.timesince import timesince
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings
import requests

def products(request):
    if request.user.is_staff:
        return redirect('adminlog')

    if request.user.is_authenticated:
        check = request.user.profile
        if check.bio == None:
            messages.info(request, "Complete profile first!")
            return redirect('account')
        else:
            pass
    else:
        pass

    products, search_query = searchProducts(request)
    custom_range, products = paginateProducts(request, products, 6)

    context = {'products': products,
               'search_query': search_query, 'custom_range': custom_range}
    return render(request, 'products/products.html', context)

def viewProduct(request, pk):
    if request.user.is_staff:
        return redirect('adminlog')
    if request.user.is_authenticated:
        check = request.user.profile
        if check.bio == None:
            messages.info(request, "Complete profile first!")
            return redirect('account')
        else:
            pass
    else:
        pass
    item = SingleProduct.objects.get(name=pk)
    products = Product.objects.filter(name=item)
    custom_range, products = paginateProducts(request, products, 6)

    context = {'products': products, 'title':pk, 'custom_range': custom_range}
    return render(request, 'products/view-product.html', context)


@login_required(login_url="login")
def checkOutProduct(request, pk):
    if request.user.is_staff:
        return redirect('adminlog')
        
    if request.user.is_authenticated:
        check = request.user.profile
        if check.bio == None:
            messages.info(request, "Complete profile first!")
            return redirect('account')
        else:
            pass
    else:
        pass
    product = Product.objects.get(id=pk)
    profile = request.user.profile
    if product.owner == profile:
        messages.info(request, 'You can not buy your own product')
        return redirect('account')
    context = {'product': product}
    return render(request, 'products/checkout.html', context)


def product(request, pk):
    if request.user.is_staff:
        return redirect('admin/')
        
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
    
    if request.user.is_staff:
        return redirect('/admin/')
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
    
    if request.user.is_staff:
        return redirect('/admin/')
    profile = request.user.profile
    product = profile.owner.get(id=pk)
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
def traderUpdate(request, pk):
    
    if request.user.is_staff:
        return redirect('/admin/')
    profile = request.user.profile
    product = profile.owner.get(id=pk)
    form = TraderProductForm(instance=product)
    
    qty = 0,
    quantity =0,

    if request.method == 'POST':
        qty= request.POST['allowedQuantity']
        quantity= request.POST['quantity']

        if quantity <= qty:


            newpayments = request.POST.get('newpayments').replace(',',  " ").split()

            form = TraderProductForm(request.POST, request.FILES, instance=product)
            if form.is_valid():

                product = form.save(commit=False)
                product.instock = True
                product.save()
                for payment in newpayments:
                    payment, created = Payment.objects.get_or_create(name=payment)
                    product.payments.add(payment)
                messages.success(request, "Done")
                return redirect('account')
            else:
                pass
                

        else:
            messages.error(request, "Quantity can not exceed {}".format(qty))
            return redirect(traderUpdate, pk=product.id)

    context = {'form': form, 'product': product}
    return render(request, "products/trader_form.html", context)






@login_required(login_url="login")
def deleteProduct(request, pk):
    
    if request.user.is_staff:
        return redirect('/admin/')
    profile = request.user.profile
    product = profile.owner.get(id=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('products')
    context = {'object': product}
    return render(request, 'delete_template.html', context)



@login_required(login_url="login")
def processOrder(request, pk):

    if request.user.is_staff:
        return redirect('/admin/')
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
        existingProduct = Product.objects.get(id=productId)
        #CHOICE MADE
        choice = request.POST['choice']

        orderId = ''
        if needQuantity <= totalQuantity:
            order = Order.objects.create(
            seller=seller,
            buyer=buyer,
            productName=productName,
            price=price,
            unity=unity,
            quantity=needQuantity,
            location=location,
            request=reason,
            ProductId=existingProduct.id)

            
                    # Get the instance of the model that you want to update
            prod = Product.objects.get(id=productId)
            identity = SingleProduct.objects.get(name=productName)



            # Update the field values of the model instance
            prod.quantity = quantity

             # # Save the changes to the database
            order.save()
            orderId = order.id
            #              #send sms message here
            # subject = 'Dear {} you received new Order'.format(seller.name)
            # message = 'One of your products got ordered check out via :\n http://192.168.43.119:8000/notification/ or https://agri-portal.up.railway.app/notification/'

            # print(seller.user.phone)
            # print(seller.name)
            # print(productName)
            data={
                    'recipients':'{}'.format(seller.user.phone),
                    'message':'Dear {} Your Product {} got new order visit :\n http://192.168.43.119:8000/notification/ or https://agri-portal.up.railway.app/notification/ '.format(*(seller.name, productName)),
                    'sender':'+250786344674'
                }

            r=requests.post(
                'https://www.intouchsms.co.rw/api/sendsms/.json',
                data,
                auth=('ared123','Ared123?')
                )
            print (r.json(), r.status_code)

            if choice == 'Resell':
                newProd = Product.objects.create(
                    id = orderId,
                    owner=buyer,
                    name=identity,
                    instock=None,
                    featured_image = prod.featured_image,
                    description=prod.description,
                    quantity=needQuantity,
                    location=location
                )
                newProd.save()
                prod.save()
                messages.success(request, 'Your {}  waits for confirmation!'.format(productName))
                return redirect('notification')
                
            elif choice == "Consuming":
                newProd = Product.objects.create(
                    id = orderId,
                    owner=buyer,
                    name=identity,
                    instock=None,
                    featured_image = prod.featured_image,
                    description=prod.description,
                    quantity=needQuantity,
                    location=location
                )
                newProd.save()
                prod.save()
                order.save()
                messages.success(request, 'Your order sent successfully!')
                return redirect('products')
            else:
                messages.error(request, 'Error for inserting order')
                return redirect('checkout-product', pk=productId)


       

        elif needQuantity >= totalQuantity:
            messages.error(request, 'Quantity can not exceed  {}'.format(totalQuantity))
            return redirect('checkout-product', pk=productId)
        elif quantity < 0:
            messages.error(request, '{}   Must be Positive number'.format(quantity))
            return redirect('checkout-product', pk=productId)

    else:
        messages.info(request, 'something went wrong!!')
        return redirect('checkout-product', pk=productId)
     


def trend(request):

    products = Product.objects.filter(instock=True)
    top = Product.objects.distinct().filter(instock=True).order_by('-quantity')
    product = SingleProduct.objects.all().distinct()
    context = {'products':products, 
                'top':top,
                'product':product
                }
    return render(request, 'products/trend.html', context)


@login_required(login_url='login')
def confirmation(request):
    
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        
        weight = request.POST.get('weight')
        orderResponse = ''

        response = request.POST.get('response')
        Decline = request.POST.get('decline')
        Confirm = request.POST.get('Confirm')
        Delete = request.POST.get('Delete')
        
        
        
        #prod = Product.objects.filter(id=order_id) #for delete to work make it get and consuming to work
        prod = Product.objects.get(id=order_id) # for resell to work and delete to work
        prod2 = Product.objects.filter(id=order_id)
        
        order = Order.objects.get(id=order_id)
        
        updateProd = Product.objects.get(id=order.ProductId)

        if Confirm :
            if prod:
                prod.instock = False
                prod.save()
            else:
                pass

            order.status = 'Confirmed'
            order.response = response
            order.save()
            
            orderResponse = 'Confirmed'
        elif Delete:
            if not prod2  == None:
                prod2.delete()
            else:
                pass
            if updateProd:
                updateProd.quantity = updateProd.quantity + int(weight)
            else:
                pass
            updateProd.save()
            
            order.delete()
            orderResponse = 'Deleted'
        elif Decline:
            
            if  not prod2 == None :
                prod2.delete()
            else:
                pass
            if updateProd:
                updateProd.quantity = updateProd.quantity + int(weight)
            else:
                pass
            updateProd.save()
            order.status = 'Declined'
            order.response = response
            order.save()
            orderResponse = 'Declined'
        else:
            pass
            
        
        data={
                'recipients':'{}'.format(order.buyer.user.phone),
                'message':'Dear {} Your order of {} received response \n it was {} visit :\n http://192.168.43.119:8000/notification/ or https://agri-portal.up.railway.app/notification/ '.format(*(order.buyer, order.productName, orderResponse)),
                'sender':'+250786344674'
            }

        r=requests.post(
            'https://www.intouchsms.co.rw/api/sendsms/.json',
            data,
            auth=('ared123','Ared123?')
            )
        print (r.json(), r.status_code)

        messages.success(request, 'Done Successfully')
        return redirect('notification')
    else:
       messages.success(request, 'Something Went Wrong')
       return redirect('notification')




def modal(request):
    
    products = Product.objects.all().distinct()
    top = Product.objects.all().distinct().order_by('-quantity')
    product = SingleProduct.objects.all().distinct()
    context = {'products':products, 
                'top':top,
                'product':product
                }
    return render(request, 'products/try.html', context)


@csrf_exempt
def submit_form(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')

        print(name)
        print(email)
        # Do something with the data (e.g., save it to the database)
        return JsonResponse({'status': 'success'})
    else:
        return render(request, 'products/try.html')

    

register = template.Library()

@register.filter
def naturaltime(value):
    return timesince(value)



