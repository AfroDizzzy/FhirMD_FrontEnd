from unittest import loader
from django.shortcuts import render
from django.http import HttpResponse


def index(request):
        context = {"latest_question_list": False}
        return render(request, "frontend/index.html", context)
    # return HttpResponse("Hello, world. You're at the polls index.")