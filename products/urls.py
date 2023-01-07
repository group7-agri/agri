from django.urls import path
from . import views

urlpatterns = [
    path('', views.products, name="products"),
    path('product/<str:pk>/', views.product, name="product"),

    path('create-product/', views.createProduct, name="create-product"),

    path('update-product/<str:pk>/', views.updateProduct, name="update-product"),
    path('view-product/<str:pk>/', views.viewProduct, name="view-product"),

    path('delete-product/<str:pk>/', views.deleteProduct, name="delete-product"),
    path('checkout-product/<str:pk>/', views.checkOutProduct, name="checkout-product"),
]
