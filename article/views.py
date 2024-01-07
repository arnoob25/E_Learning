from . import models
from django.urls import reverse
from django.shortcuts import render
from django.views.generic import CreateView, DetailView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required

# Create your views here.
class NewArticle(PermissionRequiredMixin, CreateView):
    permission_required = 'article.can_publish_article'
    raise_exception = True
    
    model = models.Article
    fields = ['title', 'body']
    template_name = 'article/new_article.html'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('article:view', kwargs={'slug': self.object.slug})

class ViewArticle(DetailView):
    model = models.Article
    template_name = 'article/view_article.html'

