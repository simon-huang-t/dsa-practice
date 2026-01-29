from collections import defaultdict

def subarrays_with_sum(nums, target):
    prefix_sum = 0
    count = 0
    sum_count_map = defaultdict(int)
    
    # Initialize with 0 to account for subarrays starting from index 0
    sum_count_map[0] = 1
    
    for num in nums:
        # Update the prefix sum
        prefix_sum += num
        
        # Check if the current prefix sum minus the target has been seen before
        # If so, it means there exists a subarray that sums up to the target
        if prefix_sum - target in sum_count_map:
            count += sum_count_map[prefix_sum - target]
        
        # Update the count of the current prefix sum
        sum_count_map[prefix_sum] += 1
    
    return count
