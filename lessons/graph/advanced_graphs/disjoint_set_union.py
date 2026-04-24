class DisjointSetUnion:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [1] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x != root_y:
            if self.rank[root_x] < self.rank[root_y]:
                self.parent[root_x] = root_y
            elif self.rank[root_x] > self.rank[root_y]:
                self.parent[root_y] = root_x
            else:
                self.parent[root_x] = root_y
                self.rank[root_y] += 1
        return root_x != root_y

dsu = DisjointSetUnion(5)
for a, b in edges:
    dsu.union(a, b)

return len(set(dsu.find(i) for i in range(n)))



#This is also possible (To consider root_a as the root with bigger size and then switch if needed. Fewer lines of code)
def union(self, a, b):
    root_a, root_b = self.find_parent(a), self.find_parent(b)
    if root_a != root_b:
        if self.sizes[root_a] < self.sizes[root_b]:
            root_a, root_b = root_b, root_a
        self.parent[root_b] = self.parent[root_a]
        self.sizes[root_a] += self.sizes[root_b]