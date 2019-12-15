from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('conjugation/<str:infinitive>/', views.conjugation, name='conjugation'),
    path('search/', views.search, name='search'),
    path('autocomplete/', views.autocomplete, name='autocomplete')
]