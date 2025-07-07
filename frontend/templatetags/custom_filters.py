from django import template

register = template.Library()

@register.filter(name='get_item')
def get_item(dictionary, key):
    """
    Allows accessing dictionary items by key in Django templates.
    Usage: {{ my_dict|get_item:my_key }}
    """
    return dictionary.get(key)

@register.filter(name='replace_char') # Changed filter name to be specific
def replace_char(value, old_char): # Changed arg name
    """
    Replaces occurrences of a single character with a space.
    Usage: {{ my_string|replace_char:"_" }}
    """
    if isinstance(value, str):
        return value.replace(old_char, " ") # Hardcoded replacement with space
    return value