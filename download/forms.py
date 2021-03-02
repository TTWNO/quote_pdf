from django import forms

class CodeForm(forms.Form):
    address = forms.CharField(label='Address', max_length=120, required=True,
        widget=forms.TextInput(
            attrs={'placeholder': 'Search your address', 'autocomplete': 'off'}
        ))
    email = forms.EmailField(label='Email', max_length=32, required=True,
        widget=forms.TextInput(
            attrs={'placeholder': 'Enter your email'}
        ))
    code = forms.CharField(label='Code', max_length=8, required=True, 
        widget=forms.TextInput(
            attrs={'placeholder': 'Enter your code'}
    ))
