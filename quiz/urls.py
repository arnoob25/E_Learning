from . import views
from django.urls import path
from django.views.generic.base import RedirectView

app_name = 'quiz'

urlpatterns = [
    path('new/', views.NewQuiz.as_view(), name = 'new'),
    path('attempt/<slug:slug>', views.AttemptQuiz.as_view(), name = 'attempt'),
    path('list/', views.ListQuizzes.as_view(), name = 'list'),

    # redirecting the users to quiz
    path('', RedirectView.as_view(pattern_name = 'quiz:list')),
]