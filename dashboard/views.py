from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def displayDashboard(request):
    context = {}

    if request.user.groups.filter(name='teacher').exists():
        return render(request, 'dashboard/teacher_dashboard.html', context = context)
    elif request.user.groups.filter(name='student').exists():
        return render(request, 'dashboard/student_dashboard.html', context=context)
    else:
        return HttpResponse('One does not simple break into my app')