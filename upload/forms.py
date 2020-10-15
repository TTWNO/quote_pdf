from django import forms
from download.models import PDF

class PDFForm(forms.ModelForm):
    class Meta:
        model = PDF
        fields = ['address_string', 'upload_file']
