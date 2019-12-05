from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    #path('verb/<slug:verb>/', views.conjugate, name='conjugate'),
    #path('search/', views.search, name='search'),
]