from django import template

register = template.Library()


@register.filter
def extract_youtube_id(youtube_link):
    """
    Given a YouTube link in this format: https://www.youtube.com/watch?v=GSmCh4DrbWY
    extract its id (GSmCh4DrbWY)
    """
    return youtube_link.split("v=")[1]


@register.simple_tag
def list_loaded_tags():
    """
    Display a comma-separated list of loaded template tags.
    """
    loaded_tags = list(register.tags.keys())  # Get the names of loaded tags
    return ", ".join(loaded_tags)


@register.simple_tag
def test_filter():
    return "Hello"
