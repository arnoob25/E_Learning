import core.constants as constants
from . import models
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView
from django.contrib.auth.mixins import PermissionRequiredMixin

# Create your views here.
class NewArticle(PermissionRequiredMixin, CreateView):
    permission_required = 'article.add_article'
    raise_exception = True
    permission_denied_message = constants.PERMISSION_DENIED_MESSAGE

    model = models.Article
    fields = ['title', 'body']
    template_name = 'article/new_article.html'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('article:view', kwargs={'slug': self.object.slug})

class ReadArticle(DetailView):
    model = models.Article
    template_name = 'article/view_article.html'

class ListArticles(ListView):
    model = models.Article
    template_name = 'article/list_of_articles.html'
    
    def get_queryset(self):
        return super().get_queryset().order_by('-created_at', 'title')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_heading'] = constants.GENERATE_PAGE_HEADING('Article')
        context['articles'] = self.get_queryset()
        context['empty_list_message'] = constants.GENERATE_EMPTY_LIST_MESSAGE('Article')
        return context