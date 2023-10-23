#!/usr/bin/env python3
"""
Module for hypermedia pagination and a Server class.
"""
import csv
import math
from typing import List, Dict, Union


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


class Server:
    """
    Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """
        Retrieve and return a page of data from the dataset.

        Args:
            page (int): Page number (1-indexed).
            page_size (int): Number of items per page.

        Returns:
            List[List]: A list of rows representing the requested page.

        Example:
            >>> server = Server()
            >>> server.get_page(1, 3)
            [['2016', 'FEMALE', 'ASIAN AND PACIFIC ISLANDER',
                'Olivia', '172', '1'],
             ['2016', 'FEMALE', 'ASIAN AND PACIFIC ISLANDER',
                 'Chloe', '112', '2'],
             ['2016', 'FEMALE', 'ASIAN AND PACIFIC ISLANDER',
                 'Sophia', '104', '3']]
        """
        assert isinstance(page, int) and page > 0
        assert isinstance(page_size, int) and page_size > 0
        dataset = self.dataset()
        start, end = index_range(page, page_size)
        return dataset[start:end]

    def get_hyper(self, page: int = 1, page_size: int = 10) -> Dict[
            str, Union[int, List[List], None]]:
        """
        Retrieve and return a hypermedia-formatted page of data.

        Args:
            page (int): Page number (1-indexed).
            page_size (int): Number of items per page.

        Returns:
            Dict[str, Union[int, List[List], None]]

        Example:
            >>> server = Server()
            >>> server.get_hyper(1, 2)
            {'page_size': 2, 'page': 1, 'data': [['2016', 'FEMALE',
                'ASIAN AND PACIFIC ISLANDER', 'Olivia', '172', '1'],
                                               ['2016', 'FEMALE',
                                                   'ASIAN
                                                   AND PACIFIC ISLANDER',
                                                   'Chloe', '112', '2']],
             'next_page': 2, 'prev_page': None, 'total_pages': 9709}
        """
        assert isinstance(page, int) and page > 0
        assert isinstance(page_size, int) and page_size > 0
        dataset = self.dataset()
        start, end = index_range(page, page_size)
        data = dataset[start:end]
        total_pages = math.ceil(len(dataset) / page_size)

        if page < total_pages:
            next_page = page + 1
        else:
            next_page = None

        if page > 1:
            prev_page = page - 1
        else:
            prev_page = None

        return {
            "page_size": page_size,
            "page": page,
            "data": data,
            "next_page": next_page,
            "prev_page": prev_page,
            "total_pages": total_pages
        }


# Example usage and testing
if __name__ == "__main__":
    server = Server()

    # Testing assertions
    try:
        should_err = server.get_page(-10, 2)
    except AssertionError:
        print("AssertionError raised with negative values")

    try:
        should_err = server.get_page(0, 0)
    except AssertionError:
        print("AssertionError raised with 0")

    try:
        should_err = server.get_page(2, 'Bob')
    except AssertionError:
        print("AssertionError raised when page and/or page_size are not ints")

    print(server.get_page(1, 3))
    print(server.get_page(3, 2))
    print(server.get_page(3000, 100))
