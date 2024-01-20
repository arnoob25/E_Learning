from . import views
from django.urls import path
from django.views.generic.base import RedirectView

app_name = 'forum'

urlpatterns = [
    path('home/', views.DisplayForumHome.as_view(), name = 'home'),
    path('question/<slug:slug>', views.DisplayQuestion.as_view(), name = 'question'),

    # redirecting users to the home
    path('', RedirectView.as_view(pattern_name = 'forum:home')),
]