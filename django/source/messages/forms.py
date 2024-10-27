from django import forms
from messages.models import Message


class MessageSendForm(forms.ModelForm):
    """
    Forms used to send messages to users.
    """
    class Meta:
        model = Message
        fields = ['text']
        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Type a message'})
        }