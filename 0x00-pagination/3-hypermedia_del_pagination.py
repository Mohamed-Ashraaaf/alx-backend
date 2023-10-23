#!/usr/bin/env python3
"""
Deletion-resilient hypermedia pagination
"""

import csv
import math
from typing import List, Dict, Union


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by sorting position, starting at 0
        """
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            truncated_dataset = dataset[:1000]
            self.__indexed_dataset = {
                i: dataset[i] for i in range(len(dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = None, page_size: int = 10) -> Dict:
        """Retrieve and return a hypermedia-formatted page of data by index.

        Args:
            index (int): The current start index of the return page.
            page_size (int): The current page size.

        Returns:
            Dict: A dictionary containing page information.

        Example:
            >>> server = Server()
            >>> server.indexed_dataset()

            >>> res = server.get_hyper_index(3, 2)
            >>> print(res)
            {'index': 3, 'data': [['2016', 'FEMALE',
                'ASIAN AND PACIFIC ISLANDER',
                'Emma', '99', '4'],
                ['2016', 'FEMALE',
                    'ASIAN AND PACIFIC ISLANDER',
                    'Emily', '99', '4']],
             'page_size': 2, 'next_index': 5}
        """
        assert isinstance(index, int) and 0 <= index < len(
                self.__indexed_dataset)
        assert isinstance(page_size, int) and page_size > 0

        next_index = index + page_size
        if next_index >= len(self.__indexed_dataset):
            next_index = None

        data = [v for k, v in sorted(self.__indexed_dataset.items()) if
                index <= k < next_index]

        return {
            "index": index,
            "data": data,
            "page_size": page_size,
            "next_index": next_index
        }


# Example usage and testing
if __name__ == "__main__":
    server = Server()
    server.indexed_dataset()

    try:
        server.get_hyper_index(300000, 100)
    except AssertionError:
        print("AssertionError raised when out of range")

    index = 3
    page_size = 2

    print("Number of items:", len(server.indexed_dataset()))

    # 1- request the first index
    res = server.get_hyper_index(index, page_size)
    print(res)

    # 2- request the next index
    next_index = res.get('next_index')
    if next_index is not None:
        res2 = server.get_hyper_index(next_index, page_size)
        print(res2)

    # 3- remove the first index
    if index in server.indexed_dataset():
        del server.indexed_dataset()[index]
    print("Number of items:", len(server.indexed_dataset()))

    # 4- request the initial index again
    res3 = server.get_hyper_index(index, page_size)
    print(res3)

    # 5- request the initial next index again
    if next_index is not None:
        res4 = server.get_hyper_index(next_index, page_size)
        print(res4)
