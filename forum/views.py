from . import forms
from . import models
from django.db.models import Count
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import FormMixin 
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required

# Create your views here.

class DisplayForumHome(FormMixin, ListView):
    model = models.Question
    template_name = 'forum/forum_home.html'
    form_class = forms.NewQuestionForm

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(answer_count = Count('answer')).order_by('-created_at') # this counts all the answers for each question

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
    
class DisplayQuestion(ListView):

    def get(self, request):
        pass

    pass