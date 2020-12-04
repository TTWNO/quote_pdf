from django.shortcuts import render, HttpResponse
from django.http import FileResponse
from django.core.mail import EmailMultiAlternatives
from .models import Address, PDF, EmailSent, DownloadAttempt
from .forms import CodeForm
from core.models import QuoteUser
from django.template.loader import render_to_string
from django.conf import settings
import ipinfo
import json
import datetime
import hashlib
import os

IPINFO_HANDLER = ipinfo.getHandler()

# https://stackoverflow.com/a/4581997
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_client_ip_info(request):
    realip = get_client_ip(request)
    handler = ipinfo.getHandler()
    details = handler.getDetails(realip)
    # needed for testing
    if settings.DEBUG and (details.ip == '127.0.0.1' or details.ip == '::1'):
        details.city = 'Local'
        details.region = 'Local'
        details.country = 'Local'
    return details

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
    email.bcc = [settings.REQUEST_BCC]
    email.body = render_to_string('download/email/quote.txt', context)
    email.attach_alternative(render_to_string('download/email/quote.html', context), 'text/html')
    with open(str(pdf.upload_file), 'rb') as f:
        content = f.read()
        email.attach(os.path.split(pdf.upload_file.name)[-1], content, 'application/octate-stream')
    email.send()

def save_email(user, addr, pdf, dt):
    EmailSent.objects.create(
        user=user,
        pdf=pdf,
        ref_code=hashlib.sha256(dt.strftime("%Y%m%d%H%M%S").encode()).hexdigest()
    )

def download(request, addrid):
    if request.method == 'POST':
        form = CodeForm(request.POST)
        if form.is_valid():
            # get addr by id
            addr = Address.objects.filter(id=addrid)
            if len(addr) == 0:
                return render(request, 'common/not-found.html')
            # only get first addr
            addr = addr[0]
            user, created = QuoteUser.objects.get_or_create(username=form.cleaned_data['email'], email=form.cleaned_data['email'])
            # disallow login for new users
            if created:
                user.set_unusable_password()
                user.save()
            # TODO: fail gracefully
            ip = get_client_ip_info(request)
            # create download attempt
            dla = DownloadAttempt.objects.create(
                user=user,
                pdf=PDF.objects.filter(address=addr).order_by('-upload_date')[0],
                ip=ip.ip,
                geolocation="{0}, {1}, {2}".format(
                    ip.city,
                    ip.region,
                    ip.country
                )
            )
            pdf = PDF.objects.filter(address=addr, code=form.cleaned_data['code']).order_by('upload_date').reverse()
            if len(pdf) == 0:
                return render(request, 'common/password-incorrect.html')
            pdf = pdf[0]
            dla.code_correct = True
            dla.save()
            # create timestamps
            dt_date = datetime.datetime.now()
            try:
                send_email(form.cleaned_data['email'], addr, pdf, dt_date)
            except Exception as e:
                print(e)
                return render(request, 'download/email-not-sent.html', {
                    'id': addrid,
                    'code': form.cleaned_data['code']
                })
            # only saves email if it sent
            save_email(user, addr, pdf, dt_date)
            # only makes successful if email is sent
            dla.email_sent = True
            dla.save()
            return render(request, 'download/email-confirm.html')
    else:
        form = CodeForm()
        return render(request, 'download/code-form.html', {
            'form': form,
            'id': addrid
        })

def download_preload(request, addid):
    if request.method == 'POST':
        code = request.POST.get('code')
        email = request.POST.get('email')
        form = CodeForm(initial={'code': code, 'email': email})
        return render(request, 'download/code-form.html', {
            'form': form,
            'id': addrid,
        })
