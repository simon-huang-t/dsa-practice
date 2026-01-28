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

'''Follow-up Questions: 
# 1. What if the window size can be at most k?
Problem statement: maximum sum of a subarray where the subarray can have at most K elements.
'''
# This is a prefix-sum + deque problem. (advanced sliding window problem)
from collections import deque

# Ok understood
def max_sum_contiguous_subarray_k_prefix_sum_deque(nums, k):
    prefix = 0
    max_sum = float('-inf')
    dq = deque()
    dq.append((0, 0)) #index, prefix_sum
    for i in range(1, n+1):
        prefix += nums[i-1]
        while dq and dq[0][0] < i - k:
            dq.popleft()
        max_sum = max(max_sum, prefix - dq[0][1])
        while dq and dq[-1][1] > prefix:
            dq.pop()
        dq.append((i, prefix))
    return max_sum


def max_sum_contiguous_subarray_k_prefix_sum_deque(nums, k):
    prefix = 0
    max_sum = float('-inf')
    dq = deque() # stores (index, prefix_sum)
    dq.append((0, 0))
    for i in range(1, n + 1):
        prefix += nums[i - 1]

        # Ensure window size is at most k. We are managing a sliding window of valid prefix indices
        # Explanations:
        # Any subarray sum from index j to i-1 is prefix[i] - prefix[j]
        # There's a constraint:
        # i - j <= k  <=>  j >= i - k
        # So while i -j > k <=> j < i - k, we remove the leftmost element
        
        # For each i, find the smallest prefix[j] where j >= k
        # Because:
        # - Bigger prefix[i]
        # - Minus smallest possible prefix before it = maximum subarray sum
        while dq and dq[0][0] < i - k:
            dq.popleft()

        # Best sum ending here
        max_sum = max(max_sum, prefix - dq[0][1])

        # Maintain increasing prefix sums
        # A larger prefix sum is always worse for future subarrays
        # So we want to pop from the back if it's bigger than the current prefix sum
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

# Examples:
# 1) To understand:
# while dq and dq[-1][1] < prefix:
#     dq.pop()
# dq.append((i, prefix))

# prefix sums so far:
# index : 0 1 2 3
# prefix: 0 5 3 7
# if we keep (1, 5):, it will never produce a better result than (2, 3)
# it is older AND larger
# so we delete it
#This is why we keep the deque monotonically increasing

# The deque stores: Best possible starting points for future subarrays
# Invariants:
# 1) Indices are increasing
# 2) Prefix sums are increasing
# 3) All indices are within k of current i
# Because of this:
# - Front =  best prefix to substract
# - Back = worse candidates we can discard

# Full Algorithm
# For each index i:
# 1. Remove prefixes that are too old (length > k)
# 2. Compute best subarray ending at i
# 3. Remove worse prefix sums from the back
# 4. Add current prefix

# for each i we want:
# prefix[i] - min(prefix[j]) where j ∈ [i-k, i-1]

# Why the Deque Exists:
# We need to:
# - Slide the valid range [i-k, i-1]
# - Query the minimum prefix in that range
# - Do it in O(1) per step

# A deque gives us:
# O(1) front access (minimum)
# O(1) amortized insert/delete
# Order + efficiency

# I have just noticed that by writing j ∈ [i-k, i-1]
# It's obvious that if j < i-k, the indices/prefixes are too old
# it would create a subarray longer than k
# so this enforces length <= k


# while dq and dq[-1][1] < prefix:
# this prefix is worse than the current one for all future subarrays
# Why?
# Larger prefix --> smaller difference
# Older index --> expires sonner
# So it's strictly dominated

# 5. Mental Shortcut:
# a) maximum subarray sum + length constraint
# --> Think prefix sums + monotonic deque
# b) no lenght constraint
# --> Think Kadane

# For prefix sums, smaller is always better

# Sliding Window Patterns:
# 1. Fixed-size window --> exactly k, simple sum, optional indices
# 2. Dynamic-size window --> variable length, positive numbers, min-length or max-length variants
# 3. Prefix + deque --> at most k, negative numbers, max sum with indices

# Don't care about order/contiguity --> Heap
# Contiguous subarrays + sliding window + monotonic tracking --> Deque


# 1. Always ask about constraints:
# Can nums be negative?
# Maximum length/k?
# Output sum only or indices?

# 2. Pick data structure by pattern:
# Fixed-size / positive dynamic --> pointers only
# Negative numbers / at most k --> deque
# Need arbitrary order / max/min anywhere --> heap

# 3. While-loop when window is dynamic: iterate until invariant breaks

# 4. Deque front = best candidate, deque back = dominated, removed

# 1-min mnemonic
# "Pointers for fixed, while for dynamic, deque for negative/at-most, Kadane for unlimited, heap only when order doesn't matter"

#  