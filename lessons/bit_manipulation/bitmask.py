from collections import defaultdict

# Example: Given a collection of items, encode them with a bitmask
def bitmask_example(items, alphabet_size=26):
    """
    items: list of elements (e.g., characters, numbers)
    alphabet_size: number of bits to use for encoding
    """
    freq = defaultdict(int)

    for item in items:
        mask = 0
        for elem in item:
            # set the bit corresponding to elem
            # elem must be mapped to 0..alphabet_size-1
            mask |= 1 << elem  
        freq[mask] += 1

    # Now freq contains counts for each unique mask
    # You can iterate to do something like "count pairs" or DP
    ans = 0
    for k in freq.values():
        ans += k * (k - 1) // 2  # Example: count pairs with same mask

    return ans
