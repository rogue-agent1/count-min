#!/usr/bin/env python3
"""count_min - Count-Min Sketch for approximate frequency estimation."""
import sys, json, hashlib

class CountMinSketch:
    def __init__(self, width=1000, depth=5):
        self.w = width; self.d = depth
        self.table = [[0]*width for _ in range(depth)]
        self.total = 0
    
    def _hash(self, item, i):
        h = hashlib.md5(f"{i}:{item}".encode()).hexdigest()
        return int(h, 16) % self.w
    
    def add(self, item, count=1):
        self.total += count
        for i in range(self.d):
            self.table[i][self._hash(item, i)] += count
    
    def estimate(self, item):
        return min(self.table[i][self._hash(item, i)] for i in range(self.d))
    
    def merge(self, other):
        for i in range(self.d):
            for j in range(self.w):
                self.table[i][j] += other.table[i][j]
        self.total += other.total

def main():
    cms = CountMinSketch(width=100, depth=5)
    items = ["apple"]*50 + ["banana"]*30 + ["cherry"]*15 + ["date"]*5
    import random; random.shuffle(items)
    for item in items: cms.add(item)
    print("Count-Min Sketch demo\n")
    for item, true in [("apple",50),("banana",30),("cherry",15),("date",5),("fig",0)]:
        est = cms.estimate(item)
        print(f"  {item:8s}: true={true:3d}, est={est:3d}, error={est-true:+d}")
    print(f"  Total: {cms.total}")

if __name__ == "__main__":
    main()
