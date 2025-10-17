from django.forms import ModelForm
from .models import Message
from django import forms


class MessageCreateForm(ModelForm):
    class Meta:
        model = Message
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded-md',
                'rows': 1,
                'placeholder': 'Enter your message here...'
            }),
        }
