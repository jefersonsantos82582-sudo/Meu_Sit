from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("api/calcular/", views.api_calcular, name="api_calcular"),
    path("api/historico/", views.api_historico, name="api_historico"),
]
