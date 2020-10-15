from sodapy import Socrata
from core.models import CalgaryAddress
from download.models import PDF
from django.shortcuts import render, HttpResponse
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
    if request.method == 'POST':
        upload_form = PDFForm(request.POST, request.FILES)
        print(upload_form.data)
        print(request.FILES)
        print(upload_form.is_valid())
        print(upload_form.cleaned_data)
        address = upload_form.cleaned_data['address_string']
        code = 'XYZ'
        name = 'quote_'+code+'.pdf'
        pdf_file = upload_form.cleaned_data['upload_file']
        addr = c.get('uwj2-d2wc',
                    where='address = "{0}"'.format(address),
                    limit=1)[0]

        # Save address
        addr = CalgaryAddress.objects.create(
            address=addr['address'],
            house_alpha=addr['house_alpha'] if 'house_alpha' in addr else '',
            street_quad=addr['street_quad'],
            street_name=addr['street_name'],
            street_type=addr['street_type']
        )
        pdf = PDF.objects.create(
                path=name,
                address=addr,
                code=code,
                upload_file=pdf_file
        )
        pdf.save()
        return HttpResponse("File saved")
    elif request.method == "GET":
        return render(request, 'upload/upload.html', {
            'form': PDFForm()
        })
