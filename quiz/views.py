from typing import Any
import constants
from . import models
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from django.contrib.auth.mixins import PermissionRequiredMixin

# Create your views here.

class NewQuiz(PermissionRequiredMixin, CreateView):
    permission_required = 'quiz.can_arrange_quiz'
    raise_exception = True
    permission_denied_message = constants.PERMISSION_DENIED_MESSAGE

    model = models.Quiz
    template_name = 'quiz/new_quiz.html'
    fields = ['subject', 'title']

    success_url = reverse_lazy('quiz:list')
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
    
class ListQuizzes(ListView):
    model = models.Quiz
    template_name = 'quiz/list_of_quizzes.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_heading'] = constants.GENERATE_PAGE_HEADING('Quizze') # returns Quizzes
        context['quizzes'] = self.get_queryset()
        context['empty_list_message'] = constants.GENERATE_EMPTY_LIST_MESSAGE('Quiz')
        return context

class AttemptQuiz(ListView):
    model = models.Quiz
    template_name = 'quiz/list_of_quizzes.html'