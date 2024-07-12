from django import forms
from .models import Subject

class SubjectSelectForm(forms.Form):
    subject = forms.ModelChoiceField(
        queryset=Subject.objects.all(),
        required=False,
        label="Fanni tanlang",
        # empty_label="Fan tanlang"
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if Subject.objects.exists():
            self.fields['subject'].initial = Subject.objects.first()