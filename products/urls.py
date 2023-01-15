from django.urls import path
from . import views

urlpatterns = [
    path('', views.products, name="products"),
    path('product/<str:pk>/', views.product, name="product"),
    path('trend/', views.trend, name="trend"),
    path('modal/', views.modal, name="modal"),
    path('confirmation/', views.confirmation, name="confirmation"),
    path('submit-form/', views.submit_form, name='submit_form'),
    path('create-product/', views.createProduct, name="create-product"),

    path('update-product/<str:pk>/', views.updateProduct, name="update-product"),
    path('trader-update/<str:pk>/', views.traderUpdate, name="trader-update"),
    
    path('view-product/<str:pk>/', views.viewProduct, name="view-product"),

    path('delete-product/<str:pk>/', views.deleteProduct, name="delete-product"),
    path('checkout-product/<str:pk>/', views.checkOutProduct, name="checkout-product"),
    path('checkout/<str:pk>/', views.processOrder, name="process-order"),

]
