from django.contrib import admin
from django.urls import include, path
from deploye import views
urlpatterns = [
    path('deploy-webhook/', views.github_webhook_deploy, name='webhook_deploy'),
    path('admin/', admin.site.urls),
]
