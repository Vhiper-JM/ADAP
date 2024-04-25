from django.urls import path
from . import views

app_name = 'Inicio_sesion'

urlpatterns = [
    path('', views.index, name='index'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('signup_business/', views.signup_business, name='signup_business'),
    path('signout/', views.signout, name='signout'),  # URL para la función de logout


]
