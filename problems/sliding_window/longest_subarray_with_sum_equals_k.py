'''
Problem:
Longest Subarray with Sum = K (warning: negatives allowed)

Key intuition (before code)

We use prefix sums because:

If 
prefix[j] - prefix[i] = k
then
the subarray (i+1 … j) sums to k

So at index j, we ask:
“Have I ever seen prefix sum = current_sum - k before?”
'''

def longest_subarray_sum_k(nums, k):
    prefix_sum = 0
    first_seen = {0: -1}  # prefix_sum -> earliest index
    max_len = 0

    for i, num in enumerate(nums):
        prefix_sum += num

        if prefix_sum - k in first_seen:
            length = i - first_seen[prefix_sum - k]
            max_len = max(max_len, length)

        # only store the first occurrence
        if prefix_sum not in first_seen:
            first_seen[prefix_sum] = i

    return max_len

# first_seen = {0: -1}
# This handles subarrays that start at index 0.
# If:
# prefix_sum == k at index i
# then:
# prefix_sum - k = 0
# So we pretend we saw sum 0 before the array started.

# Why store only the first occurrence?
# Because Earlier index → longer subarray

# Invariant:
# At every index, first_seen contains the earliest index where each prefix sum occurred.


'''
Variant 1 — Count Subarrays with Sum = K
'''
def count_subarrays_sum_k(nums, k):
    prefix_sum = 0
    count = 0
    freq = {0: 1}

    for num in nums:
        prefix_sum += num

        if prefix_sum - k in freq:
            count += freq[prefix_sum - k]

        freq[prefix_sum] = freq.get(prefix_sum, 0) + 1

    return count

# Sliding window fails because
# 1) Expanding window can reduce sum
# 2) Shrinking window can increase sum
# Prefix sum remembers history instead.

# Mental Template:
# Subarray + sum + negatives
# --> prefix_sum, hashmap, current_sum - target