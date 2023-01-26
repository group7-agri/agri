from .models import *
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse

def paginateProducts(request, products, results):

    page = request.GET.get('page')
    paginator = Paginator(products, results)

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        products = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        products = paginator.page(page)

    leftIndex = (int(page) - 4)

    if leftIndex < 1:
        leftIndex = 1

    rightIndex = (int(page) + 5)

    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex, rightIndex)

    return custom_range, products


def searchProducts(request):

    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
    
    # item = SingleProduct.objects.filter(name_icontains=search_query)
    
    # product = ''
    # products = Product.objects.filter(name__name__icontains=search_query)
    # for ite in items:
    #     product= ite.name
    user = ''
    if request.user.is_authenticated:
        user  = request.user

    payments = Payment.objects.filter(name=search_query)

    products = Product.objects.distinct().filter((
        Q(name__name__icontains=search_query) |
        Q(description__icontains=search_query) |
        Q(location__icontains=search_query) |
        Q(owner__name__icontains=search_query) |
        Q(payments__in=payments)) &
        Q(instock=True)
    )
    return products, search_query
