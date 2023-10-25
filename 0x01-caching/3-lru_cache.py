#!/usr/bin/python3
""" LRUCache module
"""

from base_caching import BaseCaching


class LRUCache(BaseCaching):
    """ LRUCache class
    Inherits from BaseCaching and is a caching system
    """

    def __init__(self):
        """ Initialize LRUCache """
        super().__init__()
        self.used_keys = []

    def put(self, key, item):
        """ Add an item in the cache """
        if key is not None and item is not None:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                lru_key = self.used_keys.pop(0)
                del self.cache_data[lru_key]
                print("DISCARD: {}".format(lru_key))
            self.used_keys.append(key)
            self.cache_data[key] = item

    def get(self, key):
        """ Get an item by key """
        if key is not None and key in self.cache_data:
            self.used_keys.remove(key)
            self.used_keys.append(key)
            return self.cache_data[key]
        return None
