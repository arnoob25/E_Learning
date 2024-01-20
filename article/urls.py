from . import views
from django.urls import path
from django.views.generic.base import RedirectView

app_name = 'article'

urlpatterns = [
    path('new/', views.NewArticle.as_view(), name = 'new'),
    path('read/<slug:slug>', views.ReadArticle.as_view(), name = 'view'),
    path('list/', views.ListArticles.as_view(), name = 'list'),

    # redirecting the users to article list
    path('', RedirectView.as_view(pattern_name = 'article:list')),
    path('read/', RedirectView.as_view(pattern_name = 'article:list')),
]