from django.shortcuts import render
import json
from frontend.models.generalCategories import generalCategories
from frontend.models.readingFromJsonFile import *

def homepage(request):
    context = {
         'items': LIST_OF_SECTIONS,
        # 'items': generalCategories,
        'page_title': 'Django Home Page'
    }
    return render(request, 'frontend/homepage.html', context)