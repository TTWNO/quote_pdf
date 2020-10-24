from django.shortcuts import render, HttpResponse
from django.http import FileResponse
from .models import Address, PDF
from .forms import CodeForm

# Create your views here.
def starter(request):
    return render(request, 'download/download-page.html', {
        'things': list(Address.objects.all())
    })

def download(request, pdfid):
    if request.method == 'POST':
        form = CodeForm(request.POST)
        if form.is_valid():
            addr = Address.objects.filter(id=pdfid)
            if len(addr) == 0:
                return render(request, 'common/not-found.html')
            addr = addr[0]
            # TODO: If same address + different code, the old file is still visible if the old code is still known
            pdf = PDF.objects.filter(address=addr, code=form.cleaned_data['code']).order_by('upload_date').reverse()
            if len(pdf) == 0:
                return render(request, 'common/password-incorrect.html')
            pdf = pdf[0]
            return FileResponse(pdf.upload_file, as_attachment=True)
    else:
        form = CodeForm()
        return render(request, 'download/code-form.html', {
            'form': form
        })
