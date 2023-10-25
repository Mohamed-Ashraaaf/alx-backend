#!/usr/bin/python3
""" FIFOCache module
"""

from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """ FIFOCache class
    Inherits from BaseCaching and is a caching system
    """

    def __init__(self):
        """ Initialize FIFOCache """
        super().__init__()
        self.queue = []

    def put(self, key, item):
        """ Add an item in the cache """
        if key is not None and item is not None:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                discarded = self.queue.pop(0)
                del self.cache_data[discarded]
                print("DISCARD: {}".format(discarded))
            self.queue.append(key)
            self.cache_data[key] = item

    def get(self, key):
        """ Get an item by key """
        if key is not None and key in self.cache_data:
            return self.cache_data[key]
        return None
