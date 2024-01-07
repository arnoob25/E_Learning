from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

class SignupForm(UserCreationForm):

    group = forms.ModelChoiceField(
        queryset = Group.objects.filter(
            name__in = ['teacher', 'student',]
        ), label = 'Signup as:', required = True, blank = False, widget=forms.RadioSelect
    )

    def save(self, commit = True):
        user = super().save(commit = False)
        if commit:
            user.save()
            user.groups.add(self.cleaned_data['group'])
        return user

    class Meta:
        model = get_user_model()
        fields = ['group', 'username', 'password1', 'password2',]
        labels = {
            'group': 'Sign up as:',
        }

    