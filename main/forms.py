from django import forms
from .models import Subject

class SubjectSelectForm(forms.Form):
    subject = forms.ModelChoiceField(queryset=Subject.objects.all(), required=True, label="Select a Subject")