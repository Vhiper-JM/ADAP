from django.urls import path
from . import views

app_name = 'Formulario'

urlpatterns = [
    path('', views.index, name='index'),
    path('userView/', views.userView, name='userView'),
    path('companyView/', views.companyView, name='companyView'),
    path('createFormView/', views.createFormView, name='createFormView'),
    path('createForm/', views.createForm, name='createForm'),
    path('createForm/', views.createForm, name='createForm'),
    path('editProfile/', views.editProfile, name='editProfile'),
    path('uploadProfilePicture/', views.uploadProfilePicture, name='uploadProfilePicture'),
]
