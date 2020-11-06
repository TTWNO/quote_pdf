from django.shortcuts import render, HttpResponse
from request.models import QuoteRequest

# Create your views here.
def index(request):
    return render(request, 'viewrequests/requests.html', {
        'requests': QuoteRequest.objects.all()
    })

def delete(request):
    print(request.POST)
    pass