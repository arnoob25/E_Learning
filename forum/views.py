from django.shortcuts import render, HttpResponse

# Create your views here.

def displayForum(request):
    return HttpResponse('<h1>Fool!</h1>')