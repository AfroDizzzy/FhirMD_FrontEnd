import json
from django.http import Http404
from django.shortcuts import redirect, render
from frontend.models.readingFromJsonFile import SAMPLE_ITEMS

def json_detail(request, item_id):
    """
    Displays the pretty-formatted JSON for a specific item by its ID.
    """
    found_item = None
    metadata = None
    for item in SAMPLE_ITEMS:
        # Assuming each item has a unique 'id' field
        if 'id' in item and item['id'] == item_id:
            found_item = item
            break

        metadata = item.get('file_metadata')
    print(metadata)
    if found_item:
        pretty_json = json.dumps(found_item, indent=4)
        context = {
            'item_id': item_id,
            'DisplayName': item_id.replace('-', ' ').replace('_', ' ').title(),
            'pretty_json': pretty_json,
            'resource_type': found_item.get('resourceType', 'N/A'),
            'file_metadata': metadata
        }
        return render(request, 'frontend/json_detail.html', context)
    else:
        raise Http404(f"Item not found with ID: {item_id}")