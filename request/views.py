from django.shortcuts import render, HttpResponse
from .forms import RequestForm

from django.conf import settings
from django.core.mail import EmailMultiAlternatives

from core.models import QuoteUser
from download.models import Address
from .models import QuoteRequest

# Create your views here.
def index(request):
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            to_addr = form.cleaned_data['email']
            address = form.cleaned_data['address']
            email = EmailMultiAlternatives()
            email.to = [to_addr]
            email.bcc = [settings.REQUEST_BBC]
            email.body = 'Somebody has requested a quote'
            try:
                email.send()
            except:
                return HttpResponse('Error', code=500)
            # if all went all, add user, address, and request to database
            # TODO: add messages
            user, user_created = QuoteUser.objects.get_or_create(username=to_addr, email=to_addr)
            addr, addr_created = Address.objects.get_or_create(address=address)
            qr, qr_created = QuoteRequest.objects.get_or_create(user=user, address=addr)
            return render(request, 'request/request.html', {
                'form': RequestForm(),
                'message': 'Thank you for requesting a quote. We will get back to you soon.'
            })
    else:
        return render(request, 'request/request.html', {
            'form': RequestForm()
        })