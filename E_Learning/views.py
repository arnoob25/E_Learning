from django.shortcuts import redirect

def redirect_to_dashboard_or_website(request):
    if request.user.is_authenticated:
        url = 'dashboard:display_dashboard'
    else:
       url = 'user_auth:login' # Later we can redirect logged out users to the website
    return redirect(url)