def site_meta(request):
    """Makes brand constants available in every template without passing
    them from every view."""
    return {
        "SITE_NAME": "LuxeStore",
        "SITE_TAGLINE": "Considered objects, quietly made.",
    }
