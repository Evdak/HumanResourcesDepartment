from django.http import HttpResponse, Http404
from django.conf import settings
from django.http.response import HttpResponse
import os
import mimetypes
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def document(request, filename):
    file_path = os.path.join(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))), f'documents/{filename}')
    print(file_path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(
                fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + \
                os.path.basename(file_path)
            return response
    raise Http404
