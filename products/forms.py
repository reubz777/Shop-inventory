from django import forms
from .models import Batch


class BatchForm(forms.ModelForm):
    class Meta:
        model = Batch
        fields = '__all__'