from typing import Any
from . import models
from django import forms
from django.forms import ModelForm, BaseFormSet

class NewQuestionForm(ModelForm):
    class Meta:
        model = models.Question
        fields = ['title']

class NewChoiceForm(ModelForm):
    class Meta:
        model = models.Choice
        fields = ['title', 'is_correct']

class BaseChoiceFormSet(BaseFormSet):
    def clean(self):
        """Checks that at least two choices have been added."""
        if any(self.errors):
            # Don't bother validating the formset unless each form is valid on its own
            return
        if len([form for form in self.forms if form.cleaned_data]) < 2:
            raise forms.ValidationError('You must add at least two choices.')