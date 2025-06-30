from django.shortcuts import render
from django.http import HttpResponse


def sections(request):
    return HttpResponse("Sections Page")