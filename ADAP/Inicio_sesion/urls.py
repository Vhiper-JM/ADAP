from django.urls import path
from . import views

urlpatterns = [

    path('', views.login, name='inicio_sesion'),
    path('postlogin/', views.postlogin, name='postlogin'),

]
