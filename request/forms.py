from django import forms

class RequestForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=32, required=True)
    address = forms.CharField(label='Address', max_length=64, required=True)
