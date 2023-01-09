from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginUser, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerUser, name="register"),

    path('', views.profiles, name="profiles"),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),
    path('account/', views.userAccount, name="account"),

    path('edit-account/', views.editAccount, name="edit-account"),

    path('create-training/', views.createTraining, name="create-training"),
    path('update-training/<str:pk>/', views.updateTraining, name="update-training"),
    path('delete-training/<str:pk>/', views.deleteTraining, name="delete-training"),

    path('inbox/', views.inbox, name="inbox"),
    path('inboxAjax/', views.inboxAjax, name="inboxAjax"),
    
    path('message/<str:pk>/', views.viewMessage, name="message"),
    path('create-message/<str:pk>/', views.createMessage, name="create-message"),

    path('feedback/', views.Feedback, name="feedback"),
    path('feedback/inquiry/<str:pk>/', views.viewInquiry, name="inquiry"),
    path('feedback/solve-inquiry/<str:pk>/', views.markSolved, name="markSolved"),
    path('feedback/create-inquiry/', views.createInquiry, name="create-inquiry"),
]
