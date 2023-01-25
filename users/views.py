from django.dispatch.dispatcher import receiver
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from datetime import datetime, timedelta
from django import template
from django.utils.timesince import timesince
from django.urls import conf
from django.db.models import Q
from .models import Profile, Message, Inquiry
from .forms import CustomUserCreationForm, ProfileForm, TrainingForm, MessageForm, InquiryForm
from .utils import searchProfiles, paginateProfiles,searchOrders
from django.http import JsonResponse
from products.models import Order, Product, SingleProduct
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings
import requests



User = settings.AUTH_USER_MODEL


def loginUser(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            pass
            # messages.error(request, 'Username does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')

        else:
            messages.error(request, 'Username OR password is incorrect')

    return render(request, 'users/login_register.html')


def logoutUser(request):
    logout(request)
    messages.info(request, 'User was logged out!')
    return redirect('login')


def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()
    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'Account created, complete profile to be found!')

            login(request, user)
            return redirect('edit-account')

        else:
            messages.success(
                request, 'An error has occurred during registration')

    context = {'page': page, 'form': form}
    return render(request, 'users/login_register.html', context)


def profiles(request):
    
   
    profiles, search_query = searchProfiles(request)

    image = ''
    # if request.user.is_authenticated:
    #     image = Profile.objects.get(user = request.user)


    custom_range, profiles = paginateProfiles(request, profiles, 12)
    context = {'profiles': profiles, 'search_query': search_query,
               'custom_range': custom_range, 'image':image}
    if request.user.is_staff:
        return redirect('admin/')

    if request.user.is_authenticated:
        check = request.user.profile
        if check.bio == None:
            
            messages.info(request, "Complete Profile to be found")
            
        else:
            pass
    else:
        pass
    return render(request, 'users/profiles.html', context)


def userProfile(request, pk):
    
    if request.user.is_staff:
        return redirect('/admin/')
    profile = Profile.objects.get(id=pk)

    training = profile.training_set.exclude(description__exact="")

    context = {'profile': profile, 'training': training}
    return render(request, 'users/user-profile.html', context)


@login_required(login_url='login')
def userAccount(request):
    if request.user.is_staff:
        return redirect('/admin/')
    profile = request.user.profile
    
    trainings = profile.training_set.all()
    products = profile.owner.all().exclude(instock=None)

    if profile.bio == '':
        messages.info(request, "Complete Profile to be found")
        return redirect('account')
    

    context = {'profile': profile, 'trainings': trainings, 'products': products}
    return render(request, 'users/account.html', context)


@login_required(login_url='login')
def editAccount(request):
    if request.user.is_staff:
        return redirect('/admin/')
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            return redirect('account')

    context = {'form': form, 'profile': profile}
    return render(request, 'users/profile_form.html', context)


@login_required(login_url='login')
def createTraining(request):
    if request.user.is_staff:
        return redirect('/admin/')
    profile = request.user.profile
    form = TrainingForm()

    if request.method == 'POST':
        form = TrainingForm(request.POST, request.FILES)
        if form.is_valid():
            training = form.save(commit=False)
            training.owner = profile
            training.save()
            messages.success(request, 'Training was added successfully!')
            return redirect('account')

    context = {'form': form}
    return render(request, 'users/training_form.html', context)


@login_required(login_url='login')
def updateTraining(request, pk):
    if request.user.is_staff:
        return redirect('/admin/')
    profile = request.user.profile
    training = profile.training_set.get(id=pk)
    form = TrainingForm(instance=training)

    if request.method == 'POST':
        form = TrainingForm(request.POST, request.FILES, instance=training)
        if form.is_valid():
            form.save()
            messages.success(request, 'Training was updated successfully!')
            return redirect('account')
        
    

    context = {'form': form}
    return render(request, 'users/training_form.html', context)


@login_required(login_url='login')
def deleteTraining(request, pk):
    if request.user.is_staff:
        return redirect('/admin/')
    profile = request.user.profile
    training = profile.training_set.get(id=pk)
    if request.method == 'POST':
        training.delete()
        messages.success(request, 'Training was deleted successfully!')
        return redirect('account')

    context = {'object': training}
    return render(request, 'delete_template.html', context)


@login_required(login_url='login')
def inbox(request):
    if request.user.is_staff:
        return redirect('/admin/')
    profile = request.user.profile
    messageRequests = profile.messages.all()
    unreadCount = messageRequests.filter(is_read=False).count()
    context = {'messageRequests': messageRequests, 'unreadCount': unreadCount}
    return render(request, 'users/inbox.html', context)


@login_required(login_url='login')
def notification(request):
    if request.user.is_staff:
        return redirect('/admin/')
    orders, search_query = searchOrders(request)
    profile = request.user.profile
    buys  = profile.buyer.all()
    product = SingleProduct.objects.all()

  
    pending = buys.filter( status__icontains ='Pending' ).count()
    confirmed = buys.filter( status__icontains ='Confirmed' ).count()
    declined = buys.filter( status__icontains ='Declined' ).count()

  
    
    context = {'pending': pending,  'confirmed': confirmed, 'declined': declined, 'product':product, 'orders':orders, 'search_query':search_query}
    return render(request, 'users/notification.html', context)


@login_required(login_url='login')
def viewMessage(request, pk):
    if request.user.is_staff:
        return redirect('/admin/')
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if message.is_read == False:
        message.is_read = True
        message.save()
    context = {'message': message}
    return render(request, 'users/message.html', context)


def createMessage(request, pk):
    
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()

    try:
        sender = request.user.profile
    except:
        sender = None

    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            if sender:
                message.name = sender.name
                message.email = sender.email
            message.save()

            messages.success(request, 'Your message was successfully sent!')
            return redirect('user-profile', pk=recipient.id)

    context = {'recipient': recipient, 'form': form}
    return render(request, 'users/message_form.html', context)



@login_required(login_url='login')
def Feedback(request):
    if not request.user.is_staff:
        return redirect('/')
    feedbacks = Inquiry.objects.all()
    unreadCount = feedbacks.filter(is_read=False).count()
    context = {'feedbacks': feedbacks, 'unreadCount': unreadCount}
    return render(request, 'users/inquiry_inbox.html', context)


@login_required(login_url='login')
def viewInquiry(request, pk):
    if not request.user.is_staff:
        return redirect('/')
    inquiry = Inquiry.objects.get(id=pk)

    if request.method == 'POST':
        reply = request.POST['message']
        inquiry.reply = reply
        inquiry.save()
                    #send sms message here
        subject = 'Dear {} your inquiry received response'.format(inquiry.name)
        message = 'We are sorry you didnt find it smooth \n\n your inquiry: ({}) \n {} a :\n http://192.168.43.119:8000/ or https://agri-portal.up.railway.app/'.format(inquiry.subject, inquiry.reply)

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [inquiry.email],
            fail_silently=False,
        )

    if inquiry.is_read == False:
        inquiry.is_read = True
        inquiry.save()
    context = {'inquiry': inquiry}
    return render(request, 'users/inquiry.html', context)

@login_required(login_url='login')
def markSolved(request, pk):
    if not request.user.is_staff:
        return redirect('/')
    inquiry = Inquiry.objects.get(id=pk)
    inquiry.status = 'Solved'
    inquiry.save()
    context = {'inquiry': inquiry}
    return redirect('feedback')


def aboutUs(request):
    form = InquiryForm()

    try:
        sender = request.user.profile
    except:
        sender = None

    if request.method == 'POST':
        form = InquiryForm(request.POST, request.FILES)
        if form.is_valid():
            inquiry = form.save(commit=False)
            inquiry.sender = sender

            if sender:
                inquiry.name = sender.name
                inquiry.email = sender.email
            inquiry.save()

            messages.success(request, 'Your Inquiry was successfully sent!')
            return redirect('profiles')

    context = {'form': form}
    return render(request, 'aboutUs.html', context)





# TODO: AJAX FUNCTIONS


@login_required(login_url='login')
def inboxAjax(request):
    profile = request.user.profile
    staff = request.user.is_staff

    messageRequests = profile.messages.all()
    buys  = profile.buyer.all()

    notifications = buys.filter( status__icontains ='Confirmed' ).count()


 
    unreadCount = messageRequests.filter(is_read=False).count()
    periods = []
    for p in messageRequests:
        period = [naturaltime(p.created)]
        periods.append(period)
    
    #context = {"messageRequests": list(messageRequests.values()), "unreadCount": list(unreadCount.values())}
    return JsonResponse({"messageRequests": list(messageRequests.values()), 'staff':staff, "unreadCount": unreadCount, "notifications": notifications, "timesent": periods})


#TODO: AI response


register = template.Library()

@register.filter
def naturaltime(value):
    return timesince(value)


@register.filter
def multiply(value, arg):
    return value * arg



