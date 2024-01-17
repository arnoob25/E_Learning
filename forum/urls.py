from . import views
from django.urls import path

app_name = 'forum'

urlpatterns = [
    path('', views.displayForum, name = 'home'),
]