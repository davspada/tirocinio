from attr import fields
from django import forms
from .models import Data

class DataForm(forms.ModelForm):

    class Meta:
        model = Data
        fields = ['path', 'frame', 'position', 'timestamp','name']