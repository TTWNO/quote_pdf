from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse_lazy
from download.models import DownloadAttempt
from datetime import datetime

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return redirect(reverse_lazy('login'))
    # TODO: Allow search
    return render(request, 'viewrequests/requests.html', {
        'requests': DownloadAttempt.objects.all().order_by('-timestamp')[:10]
    })

def csv_resp(max_items=-1):
    header = "Email,Address,IP,Geolocation,Timestamp,Valid Code,Email Sent\n"
    body = ""
    if max_items == -1:
        das = DownloadAttempt.objects.all().order_by('-timestamp')
    else:
        das = DownloadAttempt.objects.all().order_by('-timestamp')[:max_items]

    for dla in das:
        body += dla.user.email + ',' + dla.pdf.address.address + ',' + dla.ip + ',"' + dla.geolocation + '",' + dla.timestamp.strftime('%Y/%m/%d %H:%M:%S') + ',' + str(dla.code_correct) + ',' + str(dla.email_sent) + "\n"
    resp = HttpResponse(header + body, content_type='text/csv')
    resp['Content-Disposition'] = "attachment; filename=download_attempts.csv"
    return resp
    

def csv(request):
    if not request.user.is_authenticated:
        return redirect(reverse_lazy('login'))
    return csv_resp(100)

def csv_all(request):
    if not request.user.is_authenticated:
        return redirect(reverse_lazy('login'))
    return csv_resp()