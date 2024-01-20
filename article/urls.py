from . import views
from django.urls import path
from django.views.generic.base import RedirectView

app_name = 'article'

urlpatterns = [
    path('new/', views.NewArticle.as_view(), name = 'new'),
    path('view/<slug:slug>', views.ViewArticle.as_view(), name = 'view'),
    path('list/', views.ListArticles.as_view(), name = 'list'),

    # redirecting the users to article list
    path('', RedirectView.as_view(pattern_name = 'article:list')),
    path('view/', RedirectView.as_view(pattern_name = 'article:list')),
]