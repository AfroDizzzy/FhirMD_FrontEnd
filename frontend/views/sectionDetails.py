from django.http import Http404
from django.shortcuts import redirect, render
from frontend.models.readingFromJsonFile import *


def sectionDetails(request, sectionDetails):
    sectionsInCategory: list = []

    for j in SAMPLE_ITEMS:
        if j['resourceType'] == sectionDetails: 
            sectionsInCategory.append(j)
   
    if not sectionsInCategory:
        raise  Http404()
    
    context = {
        'sectionDetails': sectionsInCategory,
        'page_title': 'sections page'
    }
    return render(request, 'frontend/sectionDetails.html', context)