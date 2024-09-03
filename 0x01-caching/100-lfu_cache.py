#!/usr/bin/env python3
"""LFUCache module that inherits from BaseCaching"""
from collections import OrderedDict
BaseCaching = __import__('base_caching').BaseCaching


class LFUCache(BaseCaching):
    """ LFUCache defines a caching system with LFU eviction policy """
    def __init__(self):
        """ Initialize the cache """
        super().__init__()
        self.cache_data = OrderedDict()
        self.frequency = {}

    def put(self, key, item):
        """ Add an item in the cache """
        if key is not None and item is not None:
            if key in self.cache_data:
                self.cache_data[key] = item
                self.frequency[key] += 1
            else:
                if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                    min_freq = min(self.frequency.values())
                    least_freq_items = [k for k, v in self.frequency.items()
                                        if v == min_freq]
                    if len(least_freq_items) > 1:
                        for k in list(self.cache_data.keys()):
                            if k in least_freq_items:
                                discard = k
                                break
                    else:
                        discard = least_freq_items[0]

                    self.cache_data.pop(discard)
                    self.frequency.pop(discard)
                    print("DISCARD: {}".format(discard))

                self.cache_data[key] = item
                self.frequency[key] = 1

    def get(self, key):
        """ Get an item by key """
        if key is None or key not in self.cache_data:
            return None

        self.frequency[key] += 1

        self.cache_data.move_to_end(key, last=True)
        return self.cache_data[key]
