from django.shortcuts import render
from django.conf import settings

# Create your views here.
def index(request):
    return render(request, 'core/links.html', {
            'company': settings.COMPANY_NAME
        })
