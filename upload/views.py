from sodapy import Socrata
from core.models import CalgaryAddress
from download.models import PDF, Address
from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse_lazy
import json
from .forms import PDFForm
from django.forms import formset_factory

c = Socrata('data.calgary.ca', None)
SHORT_NAME_MAPPING = {'ALLEY': 'AL', 'AVENUE': 'AV',
                      'BAY': 'BA', 'BOULEVARD': 'BV',
                      'CAPE': 'CA', 'CENTRE': 'CE', 'CIRCLE': 'CI', 'CLOSE': 'CL', 'COMMON': 'CM', 'COURT': 'CO', 'CRESCENT': 'CR', 'COVE': 'CV',
                      'DRIVE': 'DR',
                      'GATE': 'GA', 'GARDENS': 'GD', 'GREEN': 'GR', 'GROVE': 'GV',
                      'HEATH': 'HE', 'HIGHWAY': 'HI', 'HILL': 'HL', 'HEIGHTS': 'HT',
                      'ISLAND': 'IS', 'LANDING': 'LD', 'LINK': 'LI', 'LANE': 'LN',
                      'MEWS': 'ME', 'MANOR': 'MR', 'MOUNT': 'MT',
                      'PARK': 'PA', 'PATH': 'PH', 'PLACE': 'PL', 'PARADE': 'PR', 'PASSAGE': 'PS', 'POINT': 'PT', 'PARKWAY': 'PY', 'PLAZA': 'PZ',
                      'ROAD': 'RD', 'RISE': 'RI', 'ROW': 'RO',
                      'SQUARE': 'SQ', 'STREET': 'ST',
                      'TERRACE': 'TC', 'TRAIL': 'TR',
                      'VILLAS': 'VI', 'VIEW': 'VW',
                      'WALKWAY': 'WK', 'WALK': 'WK', 'WAY': 'WY'}

def sanitize_address(addr):
    new_addr = addr.upper()
    for k,v in SHORT_NAME_MAPPING.items():
        new_addr = new_addr.replace(' ' + k, ' ' + v)
    return new_addr

def search_api(request, address):
    addrs = c.get('uwj2-d2wc',
                  where='address like "%{0}%"'.format(sanitize_address(address)),
                  limit=5)
    return HttpResponse(json.dumps(addrs))

def upload(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            upload_form = PDFForm(request.POST, request.FILES)
            files = request.FILES.getlist('files')
            if upload_form.is_valid():
                for pdf_file in files:
                    print(pdf_file)
                    filename = pdf_file.name
                    code = filename.split(".")[0].split(" ")[-1]
                    city = filename.split(".")[0].split(" ")[-2]
                    address = ' '.join(filename.split(" ")[:-1])
                    name = 'quote_'+code+'.pdf'
                    possible_match = Address.objects.filter(address=address)
                    # if address already entered
                    if len(possible_match) > 0:
                        pdf = PDF.objects.create(
                            path=name,
                            code=code,
                            upload_file=pdf_file,
                            address=possible_match[0]
                        )
                        pdf.save()
                    else: 
                        # Save new address
                        addr = Address.objects.create(
                            address=address,
                            city=city
                        )
                        # code is currently changable per file
                        pdf = PDF.objects.create(
                                path=name,
                                code=code,
                                upload_file=pdf_file,
                                address=addr
                        )
                        addr.save()
                        pdf.save()
                return HttpResponse("File(s) saved") # TODO: "x Files Saved"
        elif request.method == "GET":
            return render(request, 'upload/upload.html', {
                'form': PDFForm()
            })
    else:
        return redirect(reverse_lazy('login'))