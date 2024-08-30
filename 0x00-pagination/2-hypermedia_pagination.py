#!/usr/bin/env python3
"""This module provides functionality to paginate through a dataset
of popular baby names stored in a CSV file. The dataset is loaded
and cached by the Server class, which supports retrieving specific
pages of data based on given pagination parameters."""
import csv
import math
from typing import List, Tuple, Dict, Optional


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """
    Calculate the start and end index for pagination.

    Args:
    - page (int): The page number (1-indexed).
    - page_size (int): The number of items per page.

    Returns:
    - tuple: A tuple containing the start index and the end index.
    """
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    return (start_index, end_index)


class Server:
    """Server class to paginate a database of popular baby names.
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
        Returns a page of the dataset.

        Args:
        - page (int): The page number (1-indexed). Default is 1.
        - page_size (int): The number of items per page. Default is 10.

        Returns:
        - List[List]: The list of rows corresponding to the page of the dataset
        """
        assert type(page) == int and type(page_size) == int
        assert page > 0 and page_size > 0

        start_index, end_index = index_range(page, page_size)
        dataset = self.dataset()

        if start_index >= len(dataset):
            return []

        return dataset[start_index:end_index]

    def get_hyper(self, page: int = 1, page_size: int = 10) -> Dict:
        """
        Returns a dictionary with hypermedia pagination metadata.

        Args:
            page (int): The page number (default is 1).
            page_size (int): The number of items per page (default is 10).

        Returns:
            Dict[str, Optional[int]]: A dictionary containing pagination
            metadata, including the current page, page size, dataset page,
            total pages, and links to the next and previous pages
            (if available).
        """
        data = self.get_page(page, page_size)
        total_items = len(self.dataset())
        start_page, end_page = index_range(page, page_size)
        total_pages = math.ceil(total_items / page_size)

        hypermedia = {
            'page_size': len(data),
            'page': page,
            'data': data,
            'next_page': page + 1 if end_page < len(self.__dataset) else None,
            'prev_page': page - 1 if start_page > 0 else None,
            'total_pages': total_pages
        }

        return hypermedia
