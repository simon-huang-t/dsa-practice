def bisect_left(arr, x):
    low, high = 0, len(arr)
    
    while low < high:
        mid = (low + high) // 2
        if arr[mid] < x:
            low = mid + 1
        else:
            high = mid
    
    return low
