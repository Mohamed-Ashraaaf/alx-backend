#!/usr/bin/env python3
"""
Module for simple helper function index_range.
"""


def index_range(page: int, page_size: int) -> tuple:
    """
    Return a tuple of start and end indexes for pagination.

    Args:
        page (int): Page number (1-indexed).
        page_size (int): Number of items per page.

    Returns:
        tuple: A tuple containing the start and end indexes.

    Example:
        >>> index_range(1, 7)
        (0, 7)
    """
    start = (page - 1) * page_size
    end = page * page_size
    return (start, end)
