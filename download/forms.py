from django import forms

class CodeForm(forms.Form):
    address = forms.CharField(label='Address', max_length=120, required=True,
        widget=forms.TextInput(
            attrs={'placeholder': '123 Main St.'}
        ))
    email = forms.EmailField(label='Email', max_length=32, required=True,
        widget=forms.TextInput(
            attrs={'placeholder': 'jane@joe.com'}
        ))
    code = forms.CharField(label='Code', max_length=8, required=True, 
        widget=forms.TextInput(
            attrs={'placeholder': '123A56'}
    ))
