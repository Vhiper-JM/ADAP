from django.urls import path
from . import views

urlpatterns = [

    path('', views.login, name='inicio_sesion'),
    path('postlogin/', views.postlogin, name='postlogin'),
    path('signin/', views.signin, name='signin'),
    path('signin_business/', views.signin_business, name='signin_business'),

]
