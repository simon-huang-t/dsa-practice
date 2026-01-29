# https://leetcode.com/problems/maximum-sum-with-at-most-k-elements

import heapq
class Solution:
    def maxSum(self, grid: List[List[int]], limits: List[int], k: int) -> int:
        res = 0
        heap = []
        rows = len(grid)
        cols = len(grid[0])
        for row in grid:
            row.sort(reverse = True)
        for r in range(rows):
            for c in range(limits[r]):
                heapq.heappush(heap, grid[r][c])
                if len(heap) > k:
                    heapq.heappop(heap)
        return sum(heap)

