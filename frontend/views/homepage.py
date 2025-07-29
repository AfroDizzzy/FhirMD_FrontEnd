from django.shortcuts import render
from django.http import HttpResponse


def homepage(request):
    context = {
        "pages": {
            "sections": {
                "name": "Sections",
                "description": "Sections page ya dummy"
            },
            "sections":{
                "name": "Sssections",
                "description": "Sections page ya dummy"
            }
        
        # "references",
        # "ingrediants?" 
        }
    }
    
    return render(request, "frontend/homePage.html", context)