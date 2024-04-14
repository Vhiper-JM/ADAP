from django.urls import path
from . import views

urlpatterns = [

    path('', views.index, name='index'),
    path('<str:lang>/login', views.login, name='login'),
    path('postlogin/', views.postlogin, name='postlogin'),
    path('<str:lang>/signup/', views.signup, name='signup'),
    path('<str:lang>/signup_business/', views.signup_business, name='signup_business'),
    path('create/', views.create_user, name='create_user'),
    path('createB/', views.create_user, name='create_userB'),

]
