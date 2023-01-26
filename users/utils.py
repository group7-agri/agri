from django.db.models import Q
from .models import Profile, Training
from products.models import Order

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def paginateProfiles(request, profiles, results):
    page = request.GET.get('page')
    paginator = Paginator(profiles, results)

    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        profiles = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        profiles = paginator.page(page)

    leftIndex = (int(page) - 4)

    if leftIndex < 1:
        leftIndex = 1

    rightIndex = (int(page) + 5)

    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex, rightIndex)

    return custom_range, profiles


def searchProfiles(request):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    trainings = Training.objects.filter(trainer__icontains=search_query)

    profiles = Profile.objects.distinct().filter(
        Q(name__icontains=search_query) |
        Q(account__icontains=search_query) |
        Q(location__icontains=search_query) |
        Q(bio__icontains=search_query) |
        Q(training__in=trainings)  & 
        ~Q(user=request.user.id)
        
    )

    print(request.user.id)

    return profiles, search_query

def searchOrders(request):
    search_query = ''

    profile = request.user.profile

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

 
   

    orders = profile.buyer.filter(
        Q(productName__icontains=search_query)| 
        Q(quantity__icontains=search_query)| 
        Q(request__icontains=search_query)| 
        Q(price__icontains=search_query)| 
        Q(response__icontains=search_query)
        ) | profile.seller.filter(
        Q(productName__icontains=search_query)| 
        Q(quantity__icontains=search_query)| 
        Q(request__icontains=search_query)| 
        Q(price__icontains=search_query)| 
        Q(response__icontains=search_query)
        ).order_by('-created')

    # orders = Order.objects.filter(
    #     Q(seller=profile) | 
    #     Q(buyer=profile)| 
    #     Q(productName__icontains=search_query)| 
    #     Q(quantity__icontains=search_query)| 
    #     Q(request__icontains=search_query)| 
    #     Q(price__icontains=search_query)| 
    #     Q(response__icontains=search_query)
    #     ).order_by('-created')
    return orders, search_query
