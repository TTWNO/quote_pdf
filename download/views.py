from django.shortcuts import render, HttpResponse
from django.http import FileResponse
from .models import PDF
from .forms import CodeForm

# Create your views here.
def starter(request):
    print(list(PDF.objects.all()))
    return render(request, 'download/download-page.html', {
        'things': list(PDF.objects.all())
    })

def download(request, pdfid):
    if request.method == 'POST':
        form = CodeForm(request.POST)
        if form.is_valid():
            pdfs = PDF.objects.filter(id=pdfid)
            if len(pdfs) == 0:
                return render(request, 'common/not-found.html')
            pdf = pdfs.filter(code=form.cleaned_data['code'])
            if len(pdf) == 0:
                return render(request, 'common/password-incorrect.html')
            pdf = pdf[0]
            return FileResponse(pdf.upload_file, as_attachment=True)
    else:
        form = CodeForm()
        return render(request, 'download/code-form.html', {
            'form': form
        })
