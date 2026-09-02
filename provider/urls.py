from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('providerinfo/', views.proinfo, name="proinfo"),
    path('proeditinfo/', views.proeditinfo, name="proeditinfo"),
    path('addspot/', views.addspot, name="addspot"),
    path('mannagepark/', views.managepark, name="managepark"),
    path('parkingreservation/', views.reservation, name="reservation"),
    path('delete-parking/<int:spot_id>/', views.delete_parking, name="delete-parking"),
    path('update-reservation/<int:reservation_id>/', views.update_reservation, name='update_reservation'),
    path('delete-reservation/<int:reservation_id>/', views.delete_reservation, name='delete_reservation'),
]
