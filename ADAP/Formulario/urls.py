from django.urls import path
from . import views

app_name = 'Formulario'

urlpatterns = [
    path('', views.index, name='index'),
    path('userView/', views.userView, name='userView'),
    path('desempcontextual/', views.desempContextual, name='desempcontextual'),
    path('desempcontraproducente/', views.desempContraproducente, name='desempcontraproducente'),
    path('desemptareas/', views.desempTareas, name='desempdetareas'),
    path('estraconstructivas/', views.estraConstructivas, name='estraconstructivas'),
    path('estracomportamiento/', views.estraComportamiento, name='estradecomportamiento'),
    path('estrarecompensa/', views.estraRecompensa, name='estraderecompensa'),
]
