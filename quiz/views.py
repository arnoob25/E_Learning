import logging
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.paginator import Paginator

from django.shortcuts import get_object_or_404, get_list_or_404, redirect, render
from django.views.generic import CreateView, ListView
from django.forms import formset_factory
from django.urls import reverse

import core.constants as constants

from . import forms, models

logger = logging.getLogger(__name__)

# TODO replace Httpresponse with http403 whereever the mixin is being used


class ListQuizzes(ListView):
    model = models.Quiz
    template_name = 'quiz/list_of_quizzes.html'
    ordering = ['-created_at', 'title']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_heading'] = constants.GENERATE_PAGE_HEADING(
            'Quizze')  # returns Quizzes
        context['quizzes'] = self.get_queryset()
        context['empty_list_message'] = constants.GENERATE_EMPTY_LIST_MESSAGE(
            'Quiz')
        return context


# --- Teacher arranging a quiz ---

class NewQuiz(PermissionRequiredMixin, CreateView):

    permission_required = 'quiz.add_quiz'
    permission_denied_message = constants.PERMISSION_DENIED_MESSAGE

    model = models.Quiz
    template_name = 'quiz/new_quiz.html'
    # this will take them to the page that adds questions
    fields = ['subject', 'title']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        # type: ignore
        return reverse('quiz:new_questions', kwargs={'slug': self.object.slug}) # type: ignore

# helper method for the view: newQuestion
def save_new_questions_with_choices(request, quiz):
    """
    saves the question object along with 4 optional choice objects, in the db.
    """
    question_form = forms.NewQuestionForm(request.POST)

    ChoiceFormSet = formset_factory(
        forms.NewChoiceForm, formset=forms.BaseChoiceFormSet, extra=4)
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

@permission_required('quiz.add_quiz', raise_exception=True)
def newQuestions(request, slug): #TODO possible refactor

    quiz = get_object_or_404(
        models.Quiz,
        slug=slug,
        created_by=request.user
    )

    if request.method == 'POST' and save_new_questions_with_choices(request, quiz):
    # TODO everytime I redirect, the quiz is being fetched from db, can we eliminate this extra db hit?
        return redirect('quiz:new_questions', slug) 
    

    # get the forms
    question_form = forms.NewQuestionForm()

    # get the input fields for 4 choices
    ChoiceFormSet = formset_factory(
        forms.NewChoiceForm, formset=forms.BaseChoiceFormSet, extra=4)
    choice_formset = ChoiceFormSet()

    context = {
        'quiz': quiz,
        'question_list': models.Question.objects.filter(quiz=quiz),
        'question_form': question_form,
        'choice_formset': choice_formset,
    }

    return render(request, 'quiz/new_questions.html', context=context)


# --- teacher reviewing student attempts ---

# helper method for the view: reviewStudentAttempts
def group_attempts_by_user(quiz): 
        
        attempts = models.Attempt.objects.filter(quiz = quiz)

        attempts_grouped_by_users = {}

        for attempt in attempts:
            if attempt.attempted_by not in attempts_grouped_by_users:
                attempts_grouped_by_users[attempt.attempted_by] = [attempt]
            else:
                attempts_grouped_by_users[attempt.attempted_by].append(attempt)

        return attempts_grouped_by_users

@permission_required('quiz.add_quiz', raise_exception = True)
def reviewStudentAttempts(request, slug):

    quiz = get_object_or_404(
        models.Quiz,
        slug = slug,
        created_by = request.user
    )

    student_attempts = group_attempts_by_user(quiz)

    context = {
        'quiz' : quiz,
        'student_attempts' : student_attempts,
    }

    return render(request, 'quiz/review_student_attempts.html', context)

# --- student attempting a quiz ---

# region - helper methods for the view: attemptQuiz

def get_quiz_and_question_list(request, slug):
    """
    Gets the quiz and questions. Prefetches the choices for the questions.
    """
    try:
        quiz = models.Quiz.objects.get(slug=slug)

    except models.Quiz.DoesNotExist:
        return redirect('dashboard:display_dashboard')

    question_list = models.Question.objects.filter(
        quiz=quiz).order_by('id').prefetch_related('choice_set')

    return quiz, question_list


def get_attempt(request, quiz):
    """
    Tracks attempts made by the students.
    """
    if 'attempt_id' not in request.session:
        attempt = models.Attempt(
            quiz=quiz,
            attempted_by=request.user,
        )
        attempt.save()
        request.session['attempt_id'] = attempt.id  # type: ignore

    else:
        try:
            attempt = models.Attempt.objects.get(
                id=request.session['attempt_id']
            )
        except models.Attempt.DoesNotExist:
            return redirect('quiz:list')

    return attempt


def evaluate_and_save_response(request, attempt, page_obj):
    """
    Evaluates the response, and saves it in the db.
    """

    # getting the correct choice
    question = page_obj.object_list[0]
    choice_set = question.choice_set.all()
    correct_choice = choice_set.filter(is_correct=True)

    response_form = forms.NewResponseForm(request.POST, page_obj=page_obj)

    if response_form.is_valid():

        selected_choice = response_form.cleaned_data['choice']

        is_correct = selected_choice in correct_choice

        # saving the response in the db
        response = response_form.save(commit=False)
        response.attempt = attempt
        response.question = question
        response.is_correct = is_correct

        response.save()

        response.choice.set([selected_choice])

        return is_correct

    else:
        logger.error("Response form is not valid.")

    return False


def evaluate_attempt(attempt):
    """
    if any response is False, the attempt is unsuccessful
    """
    responses = models.Response.objects.filter(attempt=attempt)

    attempt.is_successful = not any(
        not response.is_correct for response in responses)
    attempt.save()


def control_progression(request, attempt, paginator):
    """
    Controls when the student gets to move on to the next question.
    """

    page_number = request.POST.get('page')
    current_page = paginator.get_page(int(page_number))

    is_correct = evaluate_and_save_response(request, attempt, current_page)

    if not is_correct:
        page_obj = current_page

    elif is_correct and current_page.has_next():
        page_obj = paginator.get_page(int(page_number) + 1)
        is_correct = None

    else:  # student correctly responded to the last question
        evaluate_attempt(attempt)

        if 'attempt_id' in request.session:
            del request.session['attempt_id']

        return None, None

    return page_obj, is_correct

# endregion - helper methods 

@permission_required('quiz.add_attempt', raise_exception=True)
def attemptQuiz(request, slug):
    quiz, question_list = get_quiz_and_question_list(request, slug)

    attempt = get_attempt(request, quiz)

    # ask a single question at a time
    questions_in_a_page = 1
    paginator = Paginator(question_list, questions_in_a_page)
    total_pages = paginator.num_pages
    page_obj = paginator.get_page(1)

    # handle responses to questions
    if request.method == 'POST':
        page_obj, is_correct = control_progression(request, attempt, paginator)

        if page_obj is None and is_correct is None:  # quiz has ENDED
            return redirect('quiz:summary', slug)

    else:
        is_correct = None

    context = {
        'quiz': quiz,
        'page_obj': page_obj,
        'total_pages': total_pages,
        'is_correct': is_correct,
        'response_form': forms.NewResponseForm(page_obj=page_obj),
    }

    return render(request, 'quiz/attempt_quiz.html', context)


@permission_required('quiz.add_attempt', raise_exception=True)
# TODO: refactor the code to make it more maintainable, testable, and modular
def displaySummary(request, slug):
    """
    Displays the summary of the quiz attempt.
    """
    quiz = models.Quiz.objects.prefetch_related('question_set').get(slug=slug)
    questions = quiz.question_set.all()  # type: ignore
    total_questions = int(questions.count())  # type: ignore

    attempts = models.Attempt.objects.filter(
        attempted_by=request.user,
        quiz=quiz,
    ).order_by('attempted_at').prefetch_related('response_set')

    for attempt in attempts:

        responses = attempt.response_set.all().order_by('responded_at') # type: ignore
        correct_responses = int(responses.filter(is_correct=True).count())

        attempt.questions = questions  # type: ignore
        attempt.responses = responses  # type: ignore
        attempt.correct_responses = correct_responses  # type: ignore

    context = {
        'quiz': quiz,
        'total_questions': total_questions,
        'attempt_list': attempts
    }

    return render(request, 'quiz/quiz_summary.html', context)
