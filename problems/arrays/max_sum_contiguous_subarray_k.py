'''
Problem: Max Sum Contiguous Subarray K
(Note: This is a nice problem to work on follow-up questions and invariants)

Problem Statement:
Given an array of integers nums and a number k, find the maximum sum of a contiguous subarray of size k.

Example:
Input: nums = [1, 2, 3, 4, 5], k = 3
Output: 12
Explanation: The contiguous subarray [2, 3, 4] has the maximum sum of 12.
'''
# Brute Force Approach:

def max_sum_contiguous_subarray_k_brute_force(nums, k):
    n = len(nums)
    if n < k:
        return -1
    max_sum = 0
    for i in range(n - k + 1):
        current_sum = sum(nums[i:i+k])
        max_sum = max(max_sum, current_sum)
    return max_sum

print(max_sum_contiguous_subarray_k_brute_force([1, 2, 3, 4, 5], 3))

# Time Complexity: O(n * k)
# Space Complexity: O(1)

# Optimal Approach:
# Invariant: The maximum sum of a contiguous subarray of size k is the maximum sum of a contiguous subarray of size k.

def max_sum_contiguous_subarray_k(nums, k):
    n = len(nums)   
    if n < k:
        return -1
    max_sum = 0
    current_sum = 0
    for i in range(k):
        current_sum += nums[i]
    max_sum = current_sum
    for i in range(k, n):
        current_sum += nums[i] - nums[i - k]
        max_sum = max(max_sum, current_sum)
    return max_sum

print(max_sum_contiguous_subarray_k([1, 2, 3, 4, 5], 3))

# Sliding Window Approach - Another O(n) implementation:
def max_sum_contiguous_subarray_k_sliding_window(nums, k):
    n = len(nums)
    
    window_sum = sum(nums[:k])
    max_sum = window_sum

    left = 0
    for right in range(k, n):
        window_sum += nums[right] - nums[left]
        max_sum = max(max_sum, window_sum)
        left += 1
    return max_sum

print(max_sum_contiguous_subarray_k_sliding_window([1, 2, 3, 4, 5], 3)) 

# Time Complexity: O(n)
# Space Complexity: O(1)

# Follow-up Questions: 
# 1. What if the window size can be at most k?

# This is a prefix-sum + deque problem. (advanced sliding window problem)
from collections import deque

def max_sum_contiguous_subarray_k_prefix_sum_deque(nums, k):
    prefix = 0
    max_sum = float('-inf')
    dq = deque() # stores (index, prefix_sum)
    dq.append((0, 0))
    for i in range(1, n + 1):
        prefix += nums[i - 1]

        # Ensure window size is at most k
        while dq and dq[0][0] < i - k:
            dq.popleft()

        # Best sum ending here
        max_sum = max(max_sum, prefix - dq[0][1])

        # Maintain increasing prefix sums
        while dq and dq[-1][1] < prefix:
            dq.pop()
        dq.append((i, prefix))
    return max_sum

# Time Complexity: O(n)
# Space Complexity: O(n)

# Invariant: 
# 1) dq stores prefix sums in increasing order
# 2) Old indices are removed to enforce <= k constraint
# 3) The smallest prefix sum gives the largest subarray sum




