from django.shortcuts import render
import json
from frontend.models.generalCategories import generalCategories

def homepage(request):

    context = {
        # 'items': SAMPLE_ITEMS,
        'items': generalCategories,
        'page_title': 'Django Home Page'
    }
    return render(request, 'frontend/homepage.html', context)