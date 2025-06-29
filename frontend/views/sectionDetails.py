from django.http import Http404
from django.shortcuts import redirect, render
from frontend.models.readingFromJsonFile import *
import re

def sectionDetails(request, sectionDetails):
    sectionsInCategory: list = []

# this needs to go into the startup of the program until we go into
    for j in SAMPLE_ITEMS:
        if j['resourceType'] == sectionDetails: 
            sectionsInCategory.append(j)
   
    if not sectionsInCategory:
        raise  Http404()
    
    context = {
        'sectionName': sectionDetails,
        'items': sectionsInCategory,
        'page_title': 'sections page'
    }
    return render(request, 'frontend/sectionDetails.html', context)