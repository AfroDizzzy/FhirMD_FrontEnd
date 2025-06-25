from django.shortcuts import render
from django.http import HttpResponse


def sectionDetails(request, sectionDetails):
    context = {
        'sectionDetails': sectionDetails,
        'page_title': ''
    }
    print('eeeeeeeeeeeee')
    print(sectionDetails)

    
    return render(request, 'frontend/sectionDetails.html', context)