import json
from django.shortcuts import render
from frontend.models.readingFromJsonFile import SAMPLE_ITEMS, parse_ig_notation_string # NEW: Import parse_ig_notation_string
import re

def homepage(request):
    search_query = request.GET.get('search_terms', '').strip()
    approval_filter = request.GET.get('approval', '').strip()
    certification_filter = request.GET.get('certification', '').strip()

    ig_name_filter = request.GET.get('ig_name', '').strip()
    ig_version_filter = request.GET.get('ig_version', '').strip()

    # --- Data Preparation for IG dropdowns from IG_Notation ---
    # Build a dictionary to map IG names to their unique versions
    # and also collect all unique IG names.
    igs_with_versions = {} # {'IG Name': {'version1', 'version2'}, ...} (using sets for uniqueness)
    all_unique_igs = set()

    for item in SAMPLE_ITEMS:
        metadata = item.get('file_metadata')
        if metadata:
            # Prioritize Parsed_IG_Notations if available (it should be after load_all_data)
            parsed_igs = metadata.get('Parsed_IG_Notations')
            if parsed_igs:
                for ig_entry in parsed_igs:
                    ig_name = ig_entry.get('name')
                    ig_version = ig_entry.get('version')
                    if ig_name:
                        all_unique_igs.add(ig_name)
                        if ig_version:
                            if ig_name not in igs_with_versions:
                                igs_with_versions[ig_name] = set()
                            igs_with_versions[ig_name].add(ig_version)
            else:
                # Fallback to old IG/IG_Version if Parsed_IG_Notations not present
                old_ig = metadata.get('IG')
                old_ig_version = metadata.get('IG_Version')
                if old_ig:
                    all_unique_igs.add(old_ig)
                    if old_ig_version:
                        if old_ig not in igs_with_versions:
                            igs_with_versions[old_ig] = set()
                        igs_with_versions[old_ig].add(old_ig_version)


    # Convert sets to sorted lists for template rendering
    sorted_unique_igs = sorted(list(all_unique_igs))
    for ig_name, versions_set in igs_with_versions.items():
        igs_with_versions[ig_name] = sorted(list(versions_set))
    # --- End Data Preparation ---

    # --- Filtering Logic ---
    current_filtered_items = []

    for item in SAMPLE_ITEMS:
        item_matches_filters = True

        if 'resourceType' not in item:
            continue

        # 1. Apply primary text search (search_query) to resourceType AND IG name(s)
        if search_query:
            resource_type_matches = search_query.lower() in item['resourceType'].lower()
            
            # Check search_query against all parsed IG names from IG_Notation
            ig_name_search_matches = False
            parsed_igs_for_search = item.get('file_metadata', {}).get('Parsed_IG_Notations')
            if parsed_igs_for_search:
                for ig_entry in parsed_igs_for_search:
                    if search_query.lower() in ig_entry.get('name', '').lower():
                        ig_name_search_matches = True
                        break
            # Fallback for old IG field if Parsed_IG_Notations not present
            elif 'IG' in item.get('file_metadata', {}):
                if search_query.lower() in item['file_metadata']['IG'].lower():
                    ig_name_search_matches = True


            if not (resource_type_matches or ig_name_search_matches):
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
        if item_matches_filters and ig_name_filter:
            ig_name_dropdown_matches = False
            parsed_igs_for_filter = item.get('file_metadata', {}).get('Parsed_IG_Notations')
            if parsed_igs_for_filter:
                for ig_entry in parsed_igs_for_filter:
                    if ig_name_filter.lower() == ig_entry.get('name', '').lower():
                        ig_name_dropdown_matches = True
                        break
            # Fallback for old IG field
            elif 'IG' in item.get('file_metadata', {}):
                if ig_name_filter.lower() == item['file_metadata']['IG'].lower():
                    ig_name_dropdown_matches = True

            if not ig_name_dropdown_matches:
                item_matches_filters = False

        # 5. Apply IG Version dropdown filter (ig_version_filter)
        if item_matches_filters and ig_version_filter:
            ig_version_dropdown_matches = False
            parsed_igs_for_version_filter = item.get('file_metadata', {}).get('Parsed_IG_Notations')
            if parsed_igs_for_version_filter:
                for ig_entry in parsed_igs_for_version_filter:
                    if ig_version_filter.lower() == ig_entry.get('version', '').lower():
                        ig_version_dropdown_matches = True
                        break
            # Fallback for old IG_Version field
            elif 'IG_Version' in item.get('file_metadata', {}):
                if ig_version_filter.lower() == item['file_metadata']['IG_Version'].lower():
                    ig_version_dropdown_matches = True

            if not ig_version_dropdown_matches:
                item_matches_filters = False


        if item_matches_filters:
            current_filtered_items.append(item)

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