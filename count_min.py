#!/usr/bin/env python3
"""Count-Min Sketch for frequency estimation."""
import sys, hashlib

class CountMinSketch:
    def __init__(self, width=1000, depth=5):
        self.width, self.depth = width, depth
        self.table = [[0]*width for _ in range(depth)]
        self.total = 0
    def _hashes(self, item):
        s = str(item).encode()
        for i in range(self.depth):
            h = int(hashlib.sha256(s + bytes([i])).hexdigest(), 16)
            yield i, h % self.width
    def add(self, item, count=1):
        for row, col in self._hashes(item):
            self.table[row][col] += count
        self.total += count
    def estimate(self, item):
        return min(self.table[row][col] for row, col in self._hashes(item))
    def __len__(self):
        return self.total

def test():
    cms = CountMinSketch(100, 5)
    cms.add("apple", 5)
    cms.add("banana", 3)
    cms.add("cherry", 1)
    assert cms.estimate("apple") >= 5
    assert cms.estimate("banana") >= 3
    assert cms.estimate("cherry") >= 1
    assert cms.estimate("nonexist") <= 2  # small overcount ok
    assert len(cms) == 9
    print("  count_min: ALL TESTS PASSED")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test": test()
    else: print("Count-Min Sketch — frequency estimation")
