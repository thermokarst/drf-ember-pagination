"""
    Most of this is pulled directly from DRF, with minor tweaks.
"""

from collections import OrderedDict, namedtuple

from rest_framework import pagination
from rest_framework.response import Response
from rest_framework.utils.urls import remove_query_param, replace_query_param


def _get_displayed_page_numbers(current, final):
    """
    This utility function determines a list of page numbers to display.
    This gives us a nice contextually relevant set of page numbers.
    For example:
    current=14, final=16 -> [1, None, 13, 14, 15, 16]
    This implementation gives one page to each side of the cursor,
    or two pages to the side when the cursor is at the edge, then
    ensures that any breaks between non-continous page numbers never
    remove only a single page.
    For an alernativative implementation which gives two pages to each side of
    the cursor, eg. as in GitHub issue list pagination, see:
    https://gist.github.com/tomchristie/321140cebb1c4a558b15
    """
    assert current >= 1
    assert final >= current

    if final <= 5:
        return list(range(1, final + 1))

    # We always include the first two pages, last two pages, and
    # two pages either side of the current page.
    included = {1, current - 1, current, current + 1, final}

    # If the break would only exclude a single page number then we
    # may as well include the page number instead of the break.
    if current <= 4:
        included.add(2)
        included.add(3)
    if current >= final - 3:
        included.add(final - 1)
        included.add(final - 2)

    # Now sort the page numbers and drop anything outside the limits.
    included = [
        idx for idx in sorted(list(included))
        if idx > 0 and idx <= final
    ]

    # Finally insert any `...` breaks
    if current > 4:
        included.insert(1, None)
    if current < final - 3:
        included.insert(len(included) - 1, None)
    return included


def _get_page_links(page_numbers, current):
    """
    Given a list of page numbers and `None` page breaks,
    return a list of `PageLink` objects.
    """
    page_links = []
    for page_number in page_numbers:
        if page_number is None:
            page_link = {
                'number': None,
                'is_active': False,
                'is_break': True,
            }
        else:
            page_link = {
                'number': page_number,
                'is_active': (page_number == current),
                'is_break': False,
            }
        page_links.append(page_link)
    return page_links


class CustomPageNumberPagination(pagination.PageNumberPagination):
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        base_url = self.request.build_absolute_uri()
        current = self.page.number
        final = self.page.paginator.num_pages
        page_numbers = _get_displayed_page_numbers(current, final)
        page_links = _get_page_links(page_numbers, current)

        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('pagination', page_links),
            ('results', data),
        ]))
