from django.urls import path
from . import views

urlpatterns = [
    path('finder/', views.finder, name="finder"),
    path('search-parking/', views.search_parking, name='search-parking'),
]
