from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
        ]


class CustomUserUpdateForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
        ]


class FeedbackForm(forms.Form):
    subject = forms.CharField(label="Тема обращения", widget=forms.TextInput)
    content = forms.CharField(label="Текст обращения", widget=forms.Textarea)
