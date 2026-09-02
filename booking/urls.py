from django.urls import path
from . import views

urlpatterns = [
    path('reserve/<int:spot_id>/', views.reserve_spot, name='reserve_spot'),
    path('finderreservation/', views.finderreservation, name="findreservation"),
    path('cancel-parking/<int:reservation_id>/', views.cancel_parking, name="cancel-parking"),
]
