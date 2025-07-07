import json
from django.shortcuts import render
from frontend.models.readingFromJsonFile import SAMPLE_ITEMS
import re

def homepage(request):
    search_query = request.GET.get('search_terms', '').strip()
    approval_filter = request.GET.get('approval', '').strip()
    certification_filter = request.GET.get('certification', '').strip()
    ig_name_filter = request.GET.get('ig_name', '').strip()
    ig_version_filter = request.GET.get('ig_version', '').strip()

    # --- Data Preparation for Dropdowns (no changes here from previous iteration) ---
    igs_with_versions = {}
    all_unique_igs = set()

    for item in SAMPLE_ITEMS:
        metadata = item.get('file_metadata')
        if metadata:
            ig_name = metadata.get('IG')
            ig_version = metadata.get('IG_Version')

            if ig_name:
                all_unique_igs.add(ig_name)
                if ig_version:
                    if ig_name not in igs_with_versions:
                        igs_with_versions[ig_name] = set()
                    igs_with_versions[ig_name].add(ig_version)

    sorted_unique_igs = sorted(list(all_unique_igs))
    for ig_name_key, versions_set in igs_with_versions.items(): # Changed variable name to avoid clash
        igs_with_versions[ig_name_key] = sorted(list(versions_set))
    # --- End Data Preparation ---

    # --- Filtering Logic (MODIFIED) ---
    current_filtered_items = []

    for item in SAMPLE_ITEMS:
        item_matches_filters = True

        # Ensure 'resourceType' exists for basic processing
        if 'resourceType' not in item:
            continue

        # 1. Apply primary text search (search_query) to both resourceType AND IG name
        if search_query:
            resource_type_matches = search_query.lower() in item['resourceType'].lower()
            item_ig_name_from_metadata = item.get('file_metadata', {}).get('IG', '').strip()
            ig_name_matches = search_query.lower() in item_ig_name_from_metadata.lower()

            if not (resource_type_matches or ig_name_matches):
                item_matches_filters = False


        # 2. Apply approval_filter
        if item_matches_filters and approval_filter:
            item_status = item.get('clinicalStatus', {}).get('text', '').strip()
            if approval_filter.lower() != item_status.lower():
                item_matches_filters = False

        # 3. Apply certification_filter
        if item_matches_filters and certification_filter == '1':
            item_verification = item.get('verificationStatus', {}).get('text', '').strip()
            if item_verification.lower() != 'confirmed':
                item_matches_filters = False

        # 4. Apply IG Name dropdown filter (ig_name_filter)
        # This filter is separate from the text search and applies an exact match
        if item_matches_filters and ig_name_filter:
            item_ig_name = item.get('file_metadata', {}).get('IG', '').strip()
            if ig_name_filter.lower() != item_ig_name.lower():
                item_matches_filters = False

        # 5. Apply IG Version dropdown filter (ig_version_filter)
        if item_matches_filters and ig_version_filter:
            item_ig_version = item.get('file_metadata', {}).get('IG_Version', '').strip()
            if ig_version_filter.lower() != item_ig_version.lower():
                item_matches_filters = False

        if item_matches_filters:
            current_filtered_items.append(item)

    # After all filters, regenerate the list of unique resource types (sections)
    # from the filtered items.
    display_sections = sorted(list(
        {item['resourceType'] for item in current_filtered_items if 'resourceType' in item}
    ))

    context = {
        'items': display_sections,
        'page_title': 'FHIR Australia Sections',
        'search_terms': search_query,
        'approval': approval_filter,
        'certification': certification_filter,
        'all_unique_igs': sorted_unique_igs,
        'igs_with_versions': json.dumps(igs_with_versions),
        'ig_name_filter': ig_name_filter,
        'ig_version_filter': ig_version_filter,
    }
    return render(request, 'frontend/homepage.html', context)