from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'user_auth'

urlpatterns = [
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(template_name = 'user_auth/user_auth.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
