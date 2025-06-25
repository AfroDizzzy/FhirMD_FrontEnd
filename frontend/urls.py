from django.urls import path

from .views import index, homepage, sections, sectionDetails

urlpatterns = [
    # http://127.0.0.1:8000/
    path("", homepage.homepage, name="homepage"),
    # http://127.0.0.1:8000/index
    path("index", index.index, name="index"),
    # http://127.0.0.1:8000/sections
    path("sections", sections.sections, name="sections"),

    # 
    path("sections/<str:sectionDetails>/", sectionDetails.sectionDetails, name="sectionDetails"),
]