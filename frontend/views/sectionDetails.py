from django.http import Http404
from django.shortcuts import redirect, render
from frontend.models.readingFromJsonFile import SAMPLE_ITEMS
import re
import json # Ensure json is imported for json_detail view

# Change 'sectionDetails' to 'section_name' to match urls.py
def sectionDetails(request, section_name): # <-- MODIFIED LINE
    sectionsInCategory: list = []

    for j in SAMPLE_ITEMS:
        # It's good to add a check for 'resourceType' existence here too
        if 'resourceType' in j and j['resourceType'] == section_name: # <-- Use section_name here
            sectionsInCategory.append(j)

    if not sectionsInCategory:
        raise Http404(f"No items found for section: {section_name}") # <-- Use section_name here

    context = {
        'sectionName': section_name, # <-- Pass section_name to template
        'items': sectionsInCategory,
        'page_title': 'sections page'
    }
    return render(request, 'frontend/sectionDetails.html', context)

def json_detail(request, item_id):
    """
    Displays the pretty-formatted JSON for a specific item by its ID.
    """
    found_item = None
    for item in SAMPLE_ITEMS:
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