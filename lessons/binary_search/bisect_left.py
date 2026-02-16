# Returns first index where value ≥ x.
def bisect_left(arr, x):
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] < x:
            left = mid + 1
        else:
            right = mid - 1
    
    return left

# Returns first index where value > x.
def bisect_right(arr, x):
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] <= x: # Here is the difference
            left = mid + 1
        else:
            right = mid - 1

    return left
