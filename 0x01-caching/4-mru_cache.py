#!/usr/bin/python3
""" MRUCache module
"""

from base_caching import BaseCaching


class MRUCache(BaseCaching):
    """ MRUCache class
    Inherits from BaseCaching and is a caching system
    """

    def __init__(self):
        """ Initialize MRUCache """
        super().__init__()

    def put(self, key, item):
        """ Add an item in the cache """
        if key is not None and item is not None:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                mru_key = max(self.cache_data, key=self.cache_data.get)
                del self.cache_data[mru_key]
                print("DISCARD: {}".format(mru_key))
            self.cache_data[key] = item

    def get(self, key):
        """ Get an item by key """
        if key is not None and key in self.cache_data:
            return self.cache_data[key]
        return None
