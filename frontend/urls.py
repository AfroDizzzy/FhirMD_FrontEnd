from django.urls import path
from .views.homepage import homepage
from .views.sections import sections    
from .views.sectionDetails import sectionDetails, json_detail
from .views import data_admin # Import the data_admin views

urlpatterns = [
    path("", homepage, name="homepage"),
    path("sections/", sections, name="sections"),
    path("sections/<str:section_name>/", sectionDetails, name="sectionDetails"),
    path("json_detail/<str:item_id>/", json_detail, name="json_detail"),

    # Data Admin URLs
    path("data-admin/", data_admin.data_admin_index, name="data_admin_index"),
    path("data-admin/edit/<str:json_filename>/", data_admin.data_admin_edit_metadata, name="data_admin_edit_metadata"),
    path("data-admin/export-md-zip/", data_admin.export_metadata_zip, name="data_admin_export_md_zip"), # NEW URL
]