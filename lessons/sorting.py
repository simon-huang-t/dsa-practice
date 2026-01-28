'''
Explanation of Merge Sort:

Base Case: If the array has 1 or fewer elements, it is already sorted.

Recursion: Split the array into two halves, recursively sort each half.

Merging: Merge the two sorted halves by comparing elements one by one, ensuring the result is a sorted array.

Time Complexity:

O(n log n): Splitting the array takes log n steps, and merging takes O(n) time.

Space Complexity:

O(n): Merge Sort requires additional space for the merged arrays during the merging process.
'''
def merge_sort(arr):
    # Base case: an array of length 1 is already sorted
    if len(arr) <= 1:
        return arr
    
    # Split the array in half
    mid = len(arr) // 2
    left_half = merge_sort(arr[:mid])  # Recursively sort the left half
    right_half = merge_sort(arr[mid:])  # Recursively sort the right half

    # Merge the sorted halves
    return merge(left_half, right_half)

def merge(left, right):
    sorted_arr = []
    i = j = 0
    
    # Merge the two sorted arrays
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            sorted_arr.append(left[i])
            i += 1
        else:
            sorted_arr.append(right[j])
            j += 1
    
    # If there are any elements left in left or right, add them to sorted_arr
    sorted_arr.extend(left[i:])
    sorted_arr.extend(right[j:])
    
    return sorted_arr

# Example usage:
arr = [38, 27, 43, 3, 9, 82, 10]
sorted_arr = merge_sort(arr)
print(f"Sorted array using Merge Sort: {sorted_arr}")

'''
Explanation of Quick Sort:

Base Case: If the array has 0 or 1 element, it's already sorted.

Pivot Selection: A pivot element is selected (we use the last element here, but it can be chosen differently).

Partitioning: The array is partitioned into two parts:

The left part contains elements less than the pivot.

The right part contains elements greater than or equal to the pivot.

Recursion: Recursively sort the left and right partitions and combine them with the pivot.

Time Complexity:

Best and Average Case: O(n log n), where n is the length of the array. This occurs when the pivot splits the array into roughly equal halves.

Worst Case: O(n^2), which happens when the pivot is always the smallest or largest element, leading to unbalanced partitions (e.g., in the case of a sorted or reverse-sorted array).

Space Complexity:

O(log n): In the best case, Quick Sort performs in-place partitioning and uses O(log n) space for recursion (due to the recursion depth).

O(n) in the worst case (if the recursion depth is large due to unbalanced partitions).
'''

def quick_sort(arr):
    # Base case: arrays of length 0 or 1 are already sorted
    if len(arr) <= 1:
        return arr
    
    # Choose a pivot element (can be any element; here, the last element is chosen)
    pivot = arr[-1]
    
    # Partition the array into two halves:
    # - Elements less than pivot go to the left
    # - Elements greater than pivot go to the right
    left = [x for x in arr[:-1] if x < pivot]
    right = [x for x in arr[:-1] if x >= pivot]
    
    # Recursively sort the left and right parts, then combine them with the pivot
    return quick_sort(left) + [pivot] + quick_sort(right)

# Example usage:
arr = [38, 27, 43, 3, 9, 82, 10]
sorted_arr = quick_sort(arr)
print(f"Sorted array using Quick Sort: {sorted_arr}")

'''
Key Differences:

Merge Sort is more stable and guarantees O(n log n) time complexity, but it uses O(n) extra space.

Quick Sort is faster on average and uses O(log n) space for recursion, but it can degrade to O(n^2) time complexity if the pivot selection is poor.

Both algorithms are divide and conquer, but Merge Sort is a stable sorting algorithm, while Quick Sort is typically faster in practice due to better cache performance and smaller constant factors.
'''