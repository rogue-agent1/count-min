#!/usr/bin/env python3
"""count_min - Count-Min Sketch."""
import argparse, hashlib, math, sys

class CountMinSketch:
    def __init__(self, width=1000, depth=7):
        self.w = width; self.d = depth
        self.table = [[0]*width for _ in range(depth)]
        self.total = 0
    def _hashes(self, item):
        for i in range(self.d):
            h = int(hashlib.sha256(f"{i}:{item}".encode()).hexdigest(), 16)
            yield i, h % self.w
    def add(self, item, count=1):
        for i, j in self._hashes(item): self.table[i][j] += count
        self.total += count
    def estimate(self, item):
        return min(self.table[i][j] for i, j in self._hashes(item))
    def heavy_hitters(self, threshold):
        """Items with estimated count > threshold (need external tracking)."""
        pass  # Requires external item tracking

def main():
    p = argparse.ArgumentParser(description="Count-Min Sketch")
    p.add_argument("--demo", action="store_true", default=True)
    a = p.parse_args()
    cms = CountMinSketch(1000, 7)
    import random; random.seed(42)
    # Zipf-like distribution
    items = []
    for i in range(10000):
        item = f"item_{random.choices(range(100), weights=[100/(j+1) for j in range(100)])[0]}"
        items.append(item)
        cms.add(item)
    # Check accuracy
    from collections import Counter
    actual = Counter(items)
    print("Top 10 items (actual vs estimated):")
    for item, count in actual.most_common(10):
        est = cms.estimate(item)
        err = est - count
        print(f"  {item}: actual={count} est={est} error=+{err}")
    print(f"\nTotal: {cms.total}")
    print(f"Memory: {cms.w * cms.d * 4} bytes")

if __name__ == "__main__": main()
