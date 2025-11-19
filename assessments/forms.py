from django import forms
from .models import Assessment


class AssessmentUploadForm(forms.ModelForm):
    class Meta:
        model = Assessment
        fields = ('image',)
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'})
        }