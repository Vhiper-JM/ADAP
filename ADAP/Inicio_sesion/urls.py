from django.urls import path
from . import views

app_name = 'Inicio_sesion'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('postlogin/', views.postlogin, name='postlogin'),
    path('signup/', views.signup, name='signup'),
    path('signup_business/', views.signup_business, name='signup_business'),
    path('register_user/', views.register_user, name='register_user'),
    path('register_company/', views.register_company, name='register_company'),

]
