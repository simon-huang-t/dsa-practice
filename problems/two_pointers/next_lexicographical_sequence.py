'''
https://bytebytego.com/exercises/coding-patterns/two-pointers/next-lexicographical-sequence


Intuition:
We do the smallest possible change, 
starting from the right, 
because changes on the right affect the order the least.

Solution:
Find the first dip from the right, 
swap with the next bigger character, 
then reverse the tail.
'''
def next_lexicographical_string(s: str) -> str:
    chars = list(s)
    n = len(chars)

    # 1. Find the dip
    i = n - 2
    while i >= 0 and chars[i] >= chars[i + 1]:
        i -= 1

    # If no dip, it's the last permutation
    if i < 0:
        return "".join(reversed(chars))

    # 2. Find next larger character
    j = n - 1
    while chars[j] <= chars[i]:
        j -= 1

    # 3. Swap
    chars[i], chars[j] = chars[j], chars[i]

    # 4. Reverse suffix
    chars[i + 1:] = reversed(chars[i + 1:])

    return "".join(chars)
