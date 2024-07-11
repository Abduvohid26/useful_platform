from django import forms
from .models import Subject

class SubjectSelectForm(forms.Form):
    subject = forms.ModelChoiceField(queryset=Subject.objects.all(), required=False, label="Select a Subject", initial='Fan tanlang')