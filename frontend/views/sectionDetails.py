import json
from django.http import Http404
from django.shortcuts import redirect, render
from frontend.models.readingFromJsonFile import SAMPLE_ITEMS
import re

def sectionDetails(request, section_name):
    # Retrieve all filter parameters from the request's GET query
    search_query = request.GET.get('search_terms', '').strip()
    approval_filter = request.GET.get('approval', '').strip()
    certification_filter = request.GET.get('certification', '').strip()
    ig_name_filter = request.GET.get('ig_name', '').strip()
    ig_version_filter = request.GET.get('ig_version', '').strip()

    sectionsInCategory: list = []

    for item in SAMPLE_ITEMS:
        # First, filter by the main section name (resourceType)
        if 'resourceType' not in item or item['resourceType'] != section_name:
            continue

        item_matches_all_other_filters = True

        # Now, apply all the additional filters passed from homepage, just like in homepage.py
        # 1. Apply primary text search (search_query) to both resourceType AND IG name
        if search_query:
            resource_type_matches = search_query.lower() in item['resourceType'].lower()
            item_ig_name_from_metadata = item.get('file_metadata', {}).get('IG', '').strip()
            ig_name_matches = search_query.lower() in item_ig_name_from_metadata.lower()

            if not (resource_type_matches or ig_name_matches):
                item_matches_all_other_filters = False

        # 2. Apply approval_filter
        if item_matches_all_other_filters and approval_filter:
            item_status = item.get('clinicalStatus', {}).get('text', '').strip()
            if approval_filter.lower() != item_status.lower():
                item_matches_all_other_filters = False

        # 3. Apply certification_filter
        if item_matches_all_other_filters and certification_filter == '1':
            item_verification = item.get('verificationStatus', {}).get('text', '').strip()
            if item_verification.lower() != 'confirmed':
                item_matches_all_other_filters = False

        # 4. Apply IG Name dropdown filter (ig_name_filter)
        if item_matches_all_other_filters and ig_name_filter:
            item_ig_name = item.get('file_metadata', {}).get('IG', '').strip()
            if ig_name_filter.lower() != item_ig_name.lower():
                item_matches_all_other_filters = False

        # 5. Apply IG Version dropdown filter (ig_version_filter)
        if item_matches_all_other_filters and ig_version_filter:
            item_ig_version = item.get('file_metadata', {}).get('IG_Version', '').strip()
            if ig_version_filter.lower() != item_ig_version.lower():
                item_matches_all_other_filters = False


        if item_matches_all_other_filters:
            sectionsInCategory.append(item)

    if not sectionsInCategory:
        raise Http404(f"No items found for section: {section_name} with applied filters.")

    context = {
        'sectionName': section_name,
        'items': sectionsInCategory, # These are the now doubly-filtered items
        'page_title': 'sections page',
        # NEW: Pass filter parameters to the template
        'search_terms': search_query,
        'approval_filter': approval_filter, # Use approval_filter for consistency
        'certification_filter': certification_filter, # Use certification_filter for consistency
        'ig_name_filter': ig_name_filter,
        'ig_version_filter': ig_version_filter,
    }
    return render(request, 'frontend/sectionDetails.html', context)

def json_detail(request, item_id):
    """
    Displays the pretty-formatted JSON for a specific item by its ID.
    """
    found_item = None
    for item in SAMPLE_ITEMS:
        # Assuming each item has a unique 'id' field
        if 'id' in item and item['id'] == item_id:
            found_item = item
            break

    if found_item:
        pretty_json = json.dumps(found_item, indent=4)
        context = {
            'item_id': item_id,
            'pretty_json': pretty_json,
            'resource_type': found_item.get('resourceType', 'N/A')
        }
        return render(request, 'frontend/json_detail.html', context)
    else:
        raise Http404(f"Item not found with ID: {item_id}")