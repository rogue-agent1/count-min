#!/usr/bin/env python3
"""Count-Min Sketch - Probabilistic frequency estimation with sublinear space."""
import sys, hashlib, math

class CountMinSketch:
    def __init__(self, width=1000, depth=5):
        self.w = width; self.d = depth
        self.table = [[0]*width for _ in range(depth)]; self.total = 0
    def _hash(self, item, i):
        h = hashlib.sha256(f"{i}:{item}".encode()).hexdigest()
        return int(h, 16) % self.w
    def add(self, item, count=1):
        self.total += count
        for i in range(self.d): self.table[i][self._hash(item, i)] += count
    def estimate(self, item):
        return min(self.table[i][self._hash(item, i)] for i in range(self.d))
    def heavy_hitters(self, threshold):
        return [(item, self.estimate(item)) for item in self._tracked if self.estimate(item) >= threshold * self.total]

def main():
    import random; random.seed(42)
    cms = CountMinSketch(width=100, depth=5)
    freq = {"apple": 500, "banana": 300, "cherry": 100, "date": 50, "elderberry": 20, "fig": 10, "grape": 5}
    for word, count in freq.items():
        for _ in range(count): cms.add(word)
    print(f"=== Count-Min Sketch ===\n")
    print(f"Width: {cms.w}, Depth: {cms.d}, Total: {cms.total}\n")
    for word, actual in sorted(freq.items(), key=lambda x: -x[1]):
        est = cms.estimate(word)
        err = est - actual
        print(f"  {word:12s}: actual={actual:4d} estimate={est:4d} overcount={err:+d}")
    print(f"\n  'mango' (not added): estimate={cms.estimate('mango')}")

if __name__ == "__main__":
    main()
