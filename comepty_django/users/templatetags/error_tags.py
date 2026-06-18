from django import template
from django.urls import reverse, NoReverseMatch

register = template.Library()

@register.simple_tag
def safe_url(view_name, *args, **kwargs):
    """
    Tries to resolve a URL. If it fails due to an empty string or 
    missing data, it returns an empty string instead of crashing the site.
    """
    try:
        return reverse(view_name, args=args, kwargs=kwargs)
    except NoReverseMatch:
        return ""