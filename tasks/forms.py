from django import forms
import time
from .models import Task

class TaskForm(forms.ModelForm):
    date_now = time.strftime("%Y-%m-%d")
    # time_now = time.strftime("%H-%M-%S")
    description = forms.CharField(widget=forms.Textarea(attrs={"class":"form"}))
    time = forms.TimeField(widget=forms.TimeInput(attrs={"type": "time", "step": "1"}))
    date = forms.DateField(widget=forms.DateInput(attrs={"type": "date", "min": date_now}))
    
    class Meta:
        model = Task
        fields = [
            'title',
            'description',
            'time',
            'date',
            'priority'
        ]