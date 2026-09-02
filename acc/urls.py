from django.urls import path
from . import views
urlpatterns = [
    path('',views.initial,name="inital"),
    path('account/',views.login,name="acc"),
    path('createacc/',views.createaccount,name="createacc"),
    path('forgot/',views.forgot,name='forgotpass'),
    path('otp/',views.otp,name='otp'),
    path("logout/",views.logout,name="logout"),
    path('home/',views.home,name='home'),
    path('resetpass/',views.resetpass,name="resetpass"),
    path('choice/',views.choice,name="choice"),
    path('providerinfo/',views.proinfo,name="proinfo"),
    path('proeditinfo/',views.proeditinfo,name="proeditinfo"),
    path('addspot/',views.addspot,name="addspot"),
    path('mannagepark/',views.managepark,name="managepark"),
    path('parkingreservation/',views.reservation,name="reservation"),
    path('finder/',views.finder,name="finder"),
    path('savedparking/',views.savedparking,name="savedparking"),
    path('bookmark-slot/<int:slot_id>/',views.toggle_bookmark, name='toggle_bookmark'),
    path('finderreservation/',views.finderreservation,name="findreservation"),   
    path('delete-parking/<int:spot_id>/',views.delete_parking, name="delete-parking"),
    path('reserve/<int:spot_id>/',views.reserve_spot, name='reserve_spot'),
    path('cancel-parking/<int:reservation_id>/',views.cancel_parking, name="cancel-parking"),
    path('update-reservation/<int:reservation_id>/',views.update_reservation, name='update_reservation'),
    path('delete-reservation/<int:reservation_id>/',views.delete_reservation, name='delete_reservation'),
    path('search-parking/',views.search_parking, name='search-parking'),

]