from django.shortcuts import render
# import json # Not needed in this view unless parsing JSON directly here
from frontend.models.generalCategories import generalCategories # Still imported but not used for `items`
from frontend.models.readingFromJsonFile import LIST_OF_SECTIONS # This holds your parsed sections

def homepage(request):
    search_query = request.GET.get('search_terms', '').strip() # Get the search term, default to empty string

    # Start with the full list of sections
    display_sections = LIST_OF_SECTIONS

    if search_query:
        # Filter sections based on the search query (case-insensitive)
        # Using a list comprehension for efficient filtering
        display_sections = [
            section for section in LIST_OF_SECTIONS
            if search_query.lower() in section.lower()
        ]

    context = {
        'items': display_sections, # Pass the filtered or full list
        'page_title': 'Django Home Page',
        # You might also want to pass the search_query back to the template
        # so the search box can retain its value after a search.
        'search_terms': search_query, # Pass the search query back
    }
    return render(request, 'frontend/homepage.html', context)