from django.shortcuts import render
from constants import PERMISSION_DENIED_MESSAGE
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
        raise PermissionDenied(PERMISSION_DENIED_MESSAGE)

    return render(request, template, context = context)
        