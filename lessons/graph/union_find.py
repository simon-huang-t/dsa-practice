class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n  # size of each set

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # path compression
        return self.parent[x]

    def union(self, a, b):
        ra = self.find(a)
        rb = self.find(b)
        if ra == rb:
            return False  # already connected
        # Union by size: attach smaller tree to larger
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        return True

    def connected(self, a, b):
        return self.find(a) == self.find(b)

    def set_size(self, x):
        return self.size[self.find(x)]
