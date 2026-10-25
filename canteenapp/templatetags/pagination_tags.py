"""Template helpers for templates/partials/pagination.html."""
from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def page_url(context, param, number, anchor=""):
    """Current URL with `param` set to `number`, keeping the other query parameters.

    Pages with several paginated lists (e.g. one per menu category) each use their
    own parameter, so moving through one list leaves the others where they were.
    """
    query = context["request"].GET.copy()
    query[param or "page"] = number
    return "?%s%s" % (query.urlencode(), "#" + anchor if anchor else "")


@register.simple_tag
def elided_pages(page):
    """Page numbers like 1 … 4 5 6 … 12 around the current page."""
    return page.paginator.get_elided_page_range(page.number, on_each_side=1, on_ends=1)
