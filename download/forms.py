from django import forms

class CodeForm(forms.Form):
    code = forms.CharField(label='Code', max_length=8, required=True, 
        widget=forms.TextInput(
            attrs={'placeholder': '123A56'}
    ))
    email = forms.EmailField(label='Email', max_length=32, required=True,
        widget=forms.TextInput(
            attrs={'placeholder': 'jane@joe.com'}
        ))