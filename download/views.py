from django.shortcuts import render, HttpResponse
from django.http import FileResponse
from django.core.mail import EmailMultiAlternatives
from .models import Address, PDF, EmailSent, DownloadAttempt
from .forms import CodeForm
from core.models import QuoteUser
from django.template.loader import render_to_string
import json
import datetime
import hashlib

# Create your views here.
def starter(request):
    return render(request, 'download/download-page.html', {
        'things': list(Address.objects.all())
    })

def search(request, addr):
    if len(addr) <= 3:
        return HttpResponse(json.dumps([]))
    return HttpResponse(json.dumps(
        [x.toDict() for x in Address.objects.filter(address__contains=addr)[:10]]
    ))

def send_email(to, addr, pdf, dt_date):
    # send email
    email = EmailMultiAlternatives()
    email.subject = 'Your free quote!'
    email.to = [to]
    context = {
        'address': addr.address,
        'datetime': dt_date.strftime("%d/%m/%Y %H:%M:%S")
    }
    email.body = render_to_string('download/email/quote.txt', context)
    email.attach_alternative(render_to_string('download/email/quote.html', context), 'text/html')
    with open(str(pdf.upload_file), 'rb') as f:
        content = f.read()
        email.attach(str(pdf.upload_file), content, 'application/octate-stream')
    email.send()

def save_email(user, addr, pdf, dt):
    EmailSent.objects.create(
        user=user,
        pdf=pdf,
        ref_code=hashlib.sha256(dt.strftime("%Y%m%d%H%M%S").encode()).hexdigest()
    )

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
            # create user
            user, created = QuoteUser.objects.get_or_create(username=form.cleaned_data['email'], email=form.cleaned_data['email'])
            # disallow login for new user
            if created:
                user.set_unusable_password()
                user.save()
            # create download attempt
            dla = DownloadAttempt.objects.create(
                user=user,
                pdf=pdf,
                ip=request.META.get('REMOTE_ADDR'),
                geolocation="{0}, {1}, {2}".format(
                    request.ipinfo.city,
                    request.ipinfo.region,
                    request.ipinfo.country
                )
            )
            # create timestamps
            dt_date = datetime.datetime.now()
            try:
                send_email(form.cleaned_data['email'], addr, pdf, dt_date)
            except:
                return render(request, 'download/email-not-sent.html', {
                    'id': pdfid,
                    'code': form.cleaned_data['code']
                })
            # only saves email if it sent
            save_email(user, addr, pdf, dt_date)
            # only makes successful if email is sent
            dla.successful = True
            dla.save()
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