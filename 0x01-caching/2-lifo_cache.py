#!/usr/bin/python3
""" LIFOCache module
"""

from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """ LIFOCache class
    Inherits from BaseCaching and is a caching system
    """

    def __init__(self):
        """ Initialize LIFOCache """
        super().__init__()
        self.stack = []

    def put(self, key, item):
        """ Add an item in the cache """
        if key is not None and item is not None:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                discarded = self.stack.pop()
                del self.cache_data[discarded]
                print("DISCARD: {}".format(discarded))
            self.stack.append(key)
            self.cache_data[key] = item

    def get(self, key):
        """ Get an item by key """
        if key is not None and key in self.cache_data:
            return self.cache_data[key]
        return None
