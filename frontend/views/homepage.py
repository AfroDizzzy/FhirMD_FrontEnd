from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import json

SAMPLE_ITEMS: json

with open('testData.json') as jsonFile:
    SAMPLE_ITEMS = json.load(jsonFile)

def homepage(request):
    context = {
        'items': SAMPLE_ITEMS,
        'page_title': 'Django Home Page'
    }
    return render(request, 'frontend/homepage.html', context)