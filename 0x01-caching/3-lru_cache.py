#!/usr/bin/env python3
"""LRUCache module that inherits from BaseCaching"""
from collections import OrderedDict
BaseCaching = __import__('base_caching').BaseCaching


class LRUCache(BaseCaching):
    """ LRUCache defines a caching system with LRU eviction policy """
    def __init__(self):
        """ Initialize the cache """
        super().__init__()
        self.cache_data = OrderedDict()

    def put(self, key, item):
        """ Add an item in the cache """
        if key is not None and item is not None:
            if key in self.cache_data:
                self.cache_data.pop(key)

            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                discard, _ = self.cache_data.popitem(last=False)
                print("DISCARD: {}".format(discard))

            self.cache_data[key] = item
            self.cache_data.move_to_end(key, last=True)

    def get(self, key):
        """ Get an item by key """
        if key is None or self.cache_data.get(key) is None:
            return None
        self.cache_data.move_to_end(key, last=True)
        return self.cache_data[key]
