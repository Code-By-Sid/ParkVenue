from django.urls import path
from . import views

urlpatterns = [
    path('', views.initial, name="initial"),
    path('account/', views.login, name="acc"),
    path('createacc/', views.createaccount, name="createacc"),
    path('forgot/', views.forgot, name='forgotpass'),
    path('otp/', views.otp, name='otp'),
    path("logout/", views.logout, name="logout"),
    path('resetpass/', views.resetpass, name="resetpass"),
    path('choice/', views.choice, name="choice"),
]
