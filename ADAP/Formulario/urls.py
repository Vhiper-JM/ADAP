from django.urls import path
from . import views

app_name = 'Formulario'

urlpatterns = [
    path('', views.index, name='index'),
    path('userView/', views.userView, name='userView'),

]
