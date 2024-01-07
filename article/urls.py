from django.urls import path
from . import views

app_name = 'article'

urlpatterns = [
    path('new/', views.NewArticle.as_view(), name='new'),
    path('view/<slug:slug>', views.ViewArticle.as_view(), name='view'),
]