from . import models
from django import forms

class BaseChoiceFormSet(forms.BaseFormSet):
    """
    formset factory uses it to check if at least two choices are provided by the user
    """
    def clean(self):
        """Checks that at least two choices have been added."""
        if any(self.errors):
            # Don't bother validating the formset unless each form is valid on its own
            return
        if len([form for form in self.forms if form.cleaned_data]) < 2:
            raise forms.ValidationError('You must add at least two choices.')

class NewQuestionForm(forms.ModelForm):
    class Meta:
        model = models.Question
        fields = ['title']

class NewChoiceForm(forms.ModelForm):
    class Meta:
        model = models.Choice
        fields = ['title', 'is_correct']

class NewResponseForm(forms.ModelForm):
    class Meta:
        model = models.Response
        fields = ['choice']

    def __init__(self, *args, **kwargs):
        page_obj = kwargs.pop('page_obj', None)
        super().__init__(*args, **kwargs)
    
        if page_obj:
            self.fields['choice'] = forms.ModelChoiceField(
                queryset = page_obj.object_list[0].choice_set.all(),
                widget = forms.RadioSelect,
            )
