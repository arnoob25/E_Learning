from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model

# Create your models here.

class Quiz(models.Model):
    SUBJECTS = (
        ('phy', 'Physics'),
        ('che', 'Chemistry'),
        ('math', 'Math'),
    )
    subject = models.CharField(choices = SUBJECTS, max_length = 4)
    title = models.CharField(max_length = 200)

    created_by = models.ForeignKey(get_user_model(), blank = True, on_delete = models.CASCADE)
    created_at = models.DateField(auto_now_add = True)
    slug = models.SlugField(max_length = 200, blank = True, unique = True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        permissions = [
            ('can_arrange_quiz', 'can arrange quiz'),
        ]