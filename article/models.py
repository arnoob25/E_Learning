from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model

# Create your models here.

class Article(models.Model):
    title = models.CharField(max_length=200, blank=False)
    body = models.TextField(blank=False)
    created_by = models.ForeignKey(get_user_model(), blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=200, blank=True, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title