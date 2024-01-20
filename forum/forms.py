from . import models
from django import forms

class NewQuestionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['title'].label = ''
        self.fields['body'].label = ''
    
    class Meta:
        model = models.Question
        fields = [
            'title',
            'body',
        ]
        widgets = {
            'title' : forms.TextInput(attrs = {'placeholder' : 'Enter title here',}),
            'body' : forms.Textarea(attrs = {'placeholder' : 'Enter question here'}),
        }

class NewAnswerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['body'].label = ''

    
    class Meta:
        model = models.Answer
        fields = ['body']
        widgets = {
            'body' : forms.Textarea(attrs = {'placeholder' : 'Type answer here'})
        }