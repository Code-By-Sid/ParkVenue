from django.urls import path
from . import views

urlpatterns = [
    path('savedparking/', views.savedparking, name="savedparking"),
    path('bookmark-slot/<int:slot_id>/', views.toggle_bookmark, name='toggle_bookmark'),
]
