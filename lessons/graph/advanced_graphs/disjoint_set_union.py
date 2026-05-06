class DisjointSetUnion:
    def __init__(self, n):
        """
        Initialize a disjoint-set union structure for n elements.
        
        Sets self.parent to a list [0, 1, ..., n-1] so each element is initially its own root, and sets self.rank to a list of n ones representing the initial rank/approximate tree height for each element.
        
        Parameters:
            n (int): Number of elements; elements are labeled 0 through n-1.
        """
        self.parent = list(range(n))
        self.rank = [1] * n

    def find(self, x):
        """
        Finds the representative (root) of element x and compresses the path from x to that root.
        
        Parameters:
            x (int): Element index whose set representative is requested; expected in range 0..n-1.
        
        Returns:
            int: The index of the root representative for x.
        """
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        """
        Unites the sets containing two elements using union by rank.
        
        Parameters:
            x (int): An element index in the disjoint-set.
            y (int): Another element index in the disjoint-set.
        
        Returns:
            bool: `True` if the sets were distinct and were merged, `False` otherwise.
        """
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
    """
    Merge the sets containing elements `a` and `b` using union-by-size.
    
    Parameters:
        a (int): Index of the first element.
        b (int): Index of the second element.
    
    Notes:
        If the elements are already in the same set, no changes are made. Otherwise the root of the smaller set is attached to the root of the larger set and the size of the new root is updated.
    """
    root_a, root_b = self.find_parent(a), self.find_parent(b)
    if root_a != root_b:
        if self.sizes[root_a] < self.sizes[root_b]:
            root_a, root_b = root_b, root_a
        self.parent[root_b] = self.parent[root_a]
        self.sizes[root_a] += self.sizes[root_b]