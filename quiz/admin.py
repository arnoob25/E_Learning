from . import models
from django.contrib import admin

# Register your models here.

admin.site.register(models.Quiz)
admin.site.register(models.Question)
admin.site.register(models.Choice)
admin.site.register(models.Attempt)
admin.site.register(models.Response)
