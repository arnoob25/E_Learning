from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpResponse
from . import forms
from . import models
from django.db.models import Count
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin
from django.views.generic.detail import SingleObjectMixin 
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404


# Create your views here.

class DisplayForumHome(FormMixin, ListView):
    """
    Anyone can view the questions posted in the forum. Only students get to ask questions.
    """
    model = models.Question
    form_class = forms.NewQuestionForm
    template_name = 'forum/forum_home.html'

    def get_queryset(self):
        queryset = super().get_queryset()

        # this counts all the answers for each question
        queryset = queryset.annotate(answer_count = Count('answer')).order_by('-created_at')

        return queryset

    @method_decorator(permission_required('forum.add_question', raise_exception = True)) # only logged in students can post
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        return self.form_valid(form) if form.is_valid() else self.form_invalid(form)

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('forum:home')
    
class DisplayQuestion(FormMixin, DetailView):
    """
    Teachers and other students can post answers the question.
    """
    model = models.Question
    form_class = forms.NewAnswerForm
    template_name = 'forum/question.html'

    def get_queryset(self):
        """
        Prefetch related answers for efficiency
        """
        return super().get_queryset().prefetch_related('answer_set')

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()

        answer_set = self.object.answer_set.all() # type: ignore
        context['answer_count'] = answer_set.count()
        context['answer_set'] = answer_set.order_by('-created_at') 

        return context
    
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()

        return self.form_valid(form) if form.is_valid() else self.form_invalid(form)
            
    def form_valid(self, form):
        answer =  form.save(commit = False)
        answer.question = self.object
        answer.created_by = self.request.user
        answer.save()
        return super().form_valid(form)
        
    def get_success_url(self):
        return reverse_lazy('forum:question', kwargs = {'slug' : self.object.slug}) # type: ignore