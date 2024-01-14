import logging
import constants
from . import models, forms
from django.urls import reverse
from django.forms import formset_factory
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import CreateView, ListView, DetailView

logger = logging.getLogger(__name__)

# Create your views here.

class NewQuiz(PermissionRequiredMixin, CreateView):
    permission_required = 'quiz.add_quiz'
    raise_exception = True
    permission_denied_message = constants.PERMISSION_DENIED_MESSAGE

    model = models.Quiz
    template_name = 'quiz/new_quiz.html'
    fields = ['subject', 'title'] # this will take them to the page that adds questions
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('quiz:new_questions', kwargs = {'slug': self.object.slug})

# business logic for newQuestions()
def save_new_questions_with_choices(request, quiz):
    """
    saves the question object along with 4 optional choice objects, in the db.
    """
    question_form = forms.NewQuestionForm(request.POST)

    ChoiceFormSet = formset_factory(forms.NewChoiceForm, formset=forms.BaseChoiceFormSet, extra=4)
    choice_formset = ChoiceFormSet(request.POST)

    if question_form.is_valid() and choice_formset.is_valid():
        question = question_form.save(commit=False)
        question.quiz = quiz
        question.save()

        for choice_form in choice_formset:
            if choice_form.is_valid():
                choice = choice_form.save(commit=False)
                if choice.title:
                    choice.question = question
                    choice.save()
                else:
                    logger.error("Choice title field is empty.")
            else:
                logger.error("Choice form is not valid.")
                    
        return True
    else:
        logger.error("Question form is not valid.")
        return False

@permission_required('quiz.add_question', raise_exception = True)
def newQuestions(request, slug):
    quiz = models.Quiz.objects.get(slug=slug)

    if request.user != quiz.created_by:
        return HttpResponse(constants.PERMISSION_DENIED_MESSAGE)
    

    if request.method == 'POST' and save_new_questions_with_choices(request, quiz):
        return redirect('quiz:new_questions', slug)
        
    question_form = forms.NewQuestionForm()

    ChoiceFormSet = formset_factory(forms.NewChoiceForm, formset=forms.BaseChoiceFormSet, extra=4)
    choice_formset = ChoiceFormSet()

    context = {
        'quiz': quiz,
        'question_list': models.Question.objects.filter(quiz=quiz),
        'question_form': question_form,
        'choice_formset': choice_formset,
    }

    return render(request, 'quiz/new_questions.html', context=context)
   
class ListQuizzes(ListView):
    model = models.Quiz
    template_name = 'quiz/list_of_quizzes.html'

    def get_queryset(self):
        return super().get_queryset().order_by('-created_at','title')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_heading'] = constants.GENERATE_PAGE_HEADING('Quizze') # returns Quizzes
        context['quizzes'] = self.get_queryset()
        context['empty_list_message'] = constants.GENERATE_EMPTY_LIST_MESSAGE('Quiz')
        return context

# will require a permission - only students can attempt quizzes
class AttemptQuiz(DetailView):
    model = models.Quiz
    template_name = 'quiz/list_of_quizzes.html'
