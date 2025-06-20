from django import forms
from .models import Task, Client

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'email']

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'client', 'internal_due', 'client_due', 'status']
        widgets = {
            'internal_due': forms.DateInput(attrs={'type': 'date'}),
            'client_due': forms.DateInput(attrs={'type': 'date'}),
        }
