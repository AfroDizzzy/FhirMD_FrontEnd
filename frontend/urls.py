from django.urls import path
# Import your views directly from their respective files
from .views.index import index
from .views.homepage import homepage
from .views.sections import sections as simple_sections_view # Renamed to avoid clash if you use it
from .views.sectionDetails import sectionDetails, json_detail # Import both views

urlpatterns = [
    path("", index, name="index"),
    path("homepage/", homepage, name="homepage"),
    path("sections/", simple_sections_view, name="sections_placeholder"), # If you intend to use this general sections page
    path("sections/<str:section_name>/", sectionDetails, name="sectionDetails"),
    # New URL pattern for JSON detail page
    path("json_detail/<str:item_id>/", json_detail, name="json_detail"),
]