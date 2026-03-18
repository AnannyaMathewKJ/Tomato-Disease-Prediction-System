from django import forms
from .models import UploadedImage, ProgressRecord
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UploadedImage
        fields = ['title', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Optional title'}),
        }

class ProgressForm(forms.ModelForm):
    date_time = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type':'datetime-local'}))
    class Meta:
        model = ProgressRecord
        fields = ['previous', 'latest', 'date_time', 'title']

class SignupForm(UserCreationForm):
    email = forms.EmailField(required=False)
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        widgets = {
            'username': forms.TextInput(attrs={'style':'font-size:18px; padding:8px;'})
        }
