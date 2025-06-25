from django.shortcuts import render
from django.http import HttpResponse


def sectionDetails(request, sectionDetails):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % sectionDetails)