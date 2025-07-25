import os
import json
import glob
import zipfile
import io
from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
# from django.contrib.auth.decorators import login_required, user_passes_test # Re-add these if you put auth back
# from django.contrib.auth.models import Group # Re-add if you put auth back

from ..models.readingFromJsonFile import (
    load_all_data,
    get_all_json_filenames_with_metadata_status,
    json_files_directory,
    parse_ig_notation_string # NEW: Import the helper function (not used in this file directly, but useful for context)
)

# Define the expected metadata fields that can be edited/created
METADATA_FIELDS = [
    "Author",
    "IG_Notation", # NEW
    "PHI_Check",
    "Valid_Reference_values",
    "ResourceType",
    "Placeholder1",
    "Placeholder2",
    "Notes" # NEW
]

# Create a list of tuples: (field_name_in_dict, display_name_for_label)
DISPLAY_METADATA_FIELDS = [
    (field, field.replace('_', ' ')) for field in METADATA_FIELDS
]


# Helper function for user access control (re-add if you put auth back)
# def is_data_admin(user):
#     if not user.is_authenticated:
#         return False
#     return user.is_superuser or user.groups.filter(name='Data Administrators').exists()


# @login_required # Re-add if you put auth back
# @user_passes_test(is_data_admin) # Re-add if you put auth back
def data_admin_index(request):
    """
    Lists all JSON files and indicates if they have associated metadata.
    """
    json_files_info = get_all_json_filenames_with_metadata_status()
    context = {
        'json_files': json_files_info,
        'page_title': 'Test Data Admin',
        'json_files_directory': json_files_directory
    }
    return render(request, 'frontend/data_admin/index.html', context)


# @login_required # Re-add if you put auth back
# @user_passes_test(is_data_admin) # Re-add if you put auth back
def data_admin_edit_metadata(request, json_filename):
    """
    Displays a form to edit/create metadata for a specific JSON file.
    Handles POST requests to save the metadata.
    """
    json_file_path = os.path.join(json_files_directory, json_filename)
    md_file_path = os.path.join(json_files_directory, json_filename.replace('.json', '.md'))

    if not os.path.exists(json_file_path):
        raise Http404(f"JSON file '{json_filename}' not found.")

    current_metadata = {}
    if os.path.exists(md_file_path):
        try:
            with open(md_file_path, 'r', encoding='utf-8') as f:
                current_metadata = json.load(f)
        except json.JSONDecodeError:
            print(f"Warning: Corrupted metadata file for {json_filename}. Starting fresh.")
            current_metadata = {}
        except Exception as e:
            print(f"Error reading existing metadata for {json_filename}: {e}")
            current_metadata = {}


    if request.method == 'POST':
        new_metadata = {'filename': json_filename}

        # Automatically populate ResourceType from the JSON file if available
        try:
            with open(json_file_path, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
                if 'resourceType' in json_data:
                    new_metadata['ResourceType'] = json_data['resourceType']
        except Exception as e:
            print(f"Could not read resourceType from {json_filename}: {e}")
            # Fallback to form data if JSON read fails and it was manually entered
            manual_resource_type = request.POST.get('ResourceType', '').strip()
            if manual_resource_type:
                new_metadata['ResourceType'] = manual_resource_type


        for field in METADATA_FIELDS:
            # ResourceType is handled automatically from JSON, skip if already populated
            if field == 'ResourceType' and 'ResourceType' in new_metadata:
                continue

            value = request.POST.get(field, '').strip()
            if value:
                new_metadata[field] = value

        try:
            with open(md_file_path, 'w', encoding='utf-8') as f:
                json.dump(new_metadata, f, indent=2)
            print(f"Metadata saved for {json_filename} to {md_file_path}")

            load_all_data() # Reload data to reflect changes in the main UI

            return redirect('data_admin_index')
        except Exception as e:
            print(f"Error saving metadata file {md_file_path}: {e}")
            context = {
                'json_filename': json_filename,
                'metadata_fields_display': DISPLAY_METADATA_FIELDS,
                'current_metadata': new_metadata,
                'error_message': f"Failed to save metadata: {e}",
                'page_title': f"Edit Metadata for {json_filename}"
            }
            return render(request, 'frontend/data_admin/edit_metadata.html', context)

    context = {
        'json_filename': json_filename,
        'metadata_fields_display': DISPLAY_METADATA_FIELDS,
        'current_metadata': current_metadata,
        'page_title': f"Edit Metadata for {json_filename}"
    }
    return render(request, 'frontend/data_admin/edit_metadata.html', context)


# @login_required # Re-add if you put auth back
# @user_passes_test(is_data_admin) # Re-add if you put auth back
def export_metadata_zip(request):
    """
    Creates a zip file of all .md metadata files and serves it for download.
    """
    md_files_to_zip = glob.glob(os.path.join(json_files_directory, '*.md'))

    if not md_files_to_zip:
        raise Http404("No .md metadata files found to export.")

    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
        for md_file_path in md_files_to_zip:
            arcname = os.path.basename(md_file_path)
            try:
                zf.write(md_file_path, arcname)
            except Exception as e:
                print(f"Error adding {md_file_path} to zip: {e}")

    zip_buffer.seek(0)

    response = HttpResponse(zip_buffer.getvalue(), content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="all_fhir_metadata.zip"'
    return response