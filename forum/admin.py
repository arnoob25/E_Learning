from . import models
from django.contrib import admin

# Register your models here.

admin.site.register(models.Question)

admin.site.register(models.Answer)