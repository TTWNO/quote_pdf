from django.shortcuts import render, HttpResponse
from download.models import DownloadAttempt

# Create your views here.
def index(request):
    # TODO: Allow search
    return render(request, 'viewrequests/requests.html', {
        'requests': DownloadAttempt.objects.all().order_by('-timestamp')[:100]
    })
