from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = OrderedDict()

        self.hits = 0
        self.misses = 0
        self.evictions = 0

    def get(self, key):
        if key not in self.cache:
            self.misses += 1
            return None

        self.hits += 1
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)

        self.cache[key] = value

        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)
            self.evictions += 1

    def stats(self):
        total = self.hits + self.misses

        return {
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": self.hits / total if total else 0,
            "evictions": self.evictions,
            "cached_queries": len(self.cache)
        }
    def reset(self):
        self.cache.clear()
        self.hits = 0
        self.misses = 0
        self.evictions = 0