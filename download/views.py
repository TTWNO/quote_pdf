from django.shortcuts import render, HttpResponse 
from django.http import FileResponse
from django.core.mail import EmailMessage
from .models import Address, PDF
from .forms import CodeForm
from core.models import QuoteUser
import json

# Create your views here.
def starter(request):
    return render(request, 'download/download-page.html', {
        'things': list(Address.objects.all())
    })

def search(request, addr):
    if len(addr) <= 3:
        return HttpResponse(json.dumps([]))
    return HttpResponse(json.dumps(
        [x.toDict() for x in Address.objects.filter(address__startswith=addr)]
    ))

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
            # save email in database; do nothing if exception
            try:
                user = QuoteUser.objects.create(username=form.cleaned_data['email'], email=form.cleaned_data['email'])
                # disallow login for user
                user.set_unusable_password()
                user.save()
            except:
                pass
            # send email
            email = EmailMessage()
            email.subject = 'Your Free Quote!'
            email.to = [form.cleaned_data['email']]
            email.body = 'Your free quote is attached to this email. This quote is valid for 30 days.'
            try:
                f = open(str(pdf.upload_file), 'rb')
                content = f.read()
                email.attach(str(pdf.upload_file), content, 'application/octate-stream')
                email.send()
            except:
                return render(request, 'download/email-not-sent.html', {
                    'id': pdfid,
                    'code': form.cleaned_data['code']
                })
            return render(request, 'download/email-confirm.html')
    else:
        form = CodeForm()
        return render(request, 'download/code-form.html', {
            'form': form,
            'id': pdfid
        })

def download_preload(request, pdfid):
    if request.method == 'POST':
        code = request.POST.get('code')
        email = request.POST.get('email')
        form = CodeForm(initial={'code': code, 'email': email})
        return render(request, 'download/code-form.html', {
            'form': form,
            'id': pdfid,
        })