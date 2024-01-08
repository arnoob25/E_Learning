from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

# Create your views here.

@login_required
def displayDashboard(request):
    context = {}
    user = request.user

    if request.user.groups.filter(name='teacher').exists():
        template = 'dashboard/teacher_dashboard.html'
    elif request.user.groups.filter(name='student').exists():
        template = 'dashboard/student_dashboard.html'
    else:
        raise PermissionDenied("You do not have permission to view this page.")

    return render(request, template, context = context)
        