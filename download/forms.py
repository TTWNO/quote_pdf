from django import forms

class CodeForm(forms.Form):
    code = forms.CharField(label='Code', max_length=8, required=True)
