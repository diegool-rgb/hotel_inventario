from django.urls import path
from . import views

app_name = 'reportes'

urlpatterns = [
    path('', views.lista_reportes, name='lista'),
]
