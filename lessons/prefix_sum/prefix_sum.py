def prefix_sum(nums):
    n = len(nums)
    prefix_sum = [0] * (n + 1)
    for i in range(n):
        prefix_sum[i + 1] = prefix_sum[i] + nums[i]
    return prefix_sum

# To calculate the sum of a subarray between indexes i and j
# prefix[j + 1] - prefix[i]

# 2nd Implementation
def prefix_sum(nums):
    n = len(nums)
    prefix_sum = [0]
    for i, num in enumerate(nums):
        prefix_sum.append(prefix_sum[-1] + num)
    return prefix_sum