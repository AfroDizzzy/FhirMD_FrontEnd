from django.shortcuts import render
from django.http import HttpResponse


def homepage(request):
    context = {"latest_question_list": False}
    return render(request, "frontend/homePage.html", context)