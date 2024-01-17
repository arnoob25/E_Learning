from . import views
from django.urls import path
from django.views.generic.base import RedirectView

app_name = 'quiz'

urlpatterns = [
    # teacher - arranging the quiz
    path('new/', views.NewQuiz.as_view(), name = 'new_quiz'),
    path('new/<slug:slug>', views.newQuestions, name = 'new_questions'),
    
    # student - attempting the quiz
    path('attempt/<slug:slug>', views.attemptQuiz, name = 'attempt'),
    path('summary/<slug:slug>', views.displaySummary, name = 'summary'),

    # all users
    path('list/', views.ListQuizzes.as_view(), name = 'list'),

    # redirecting the users to quiz
    path('', RedirectView.as_view(pattern_name = 'quiz:list')),
    path('new/', RedirectView.as_view(pattern_name = 'quiz:new_quiz')),
]