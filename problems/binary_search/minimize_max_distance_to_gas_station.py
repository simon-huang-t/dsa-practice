'''
https://leetcode.com/problems/minimize-max-distance-to-gas-station/description/

Problem Statement:
You are given an integer array stations that represents the positions of the gas stations on the x-axis. 
You are also given an integer k.

You should add k new gas stations to the array stations such that the maximum distance between any two adjacent gas stations is minimized.

Return the smallest possible maximum distance between any two adjacent gas stations after adding the k new gas stations.

Examples:
Input: stations = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], K = 9
Output: 0.500000
Explanation: The optimal way is to add the 9 new gas stations at positions 2, 3, 4, 5, 6, 7, 8, 9, and 10.
'''


'''
Step 1: Ask yourself
What's the answer space?
The maximum distance between adjacent stations.
Min = 0, Max = stations[-1] - stations[0].

What's the feasibility function?
Can we add ≤ K stations so that the maximum distance between adjacent stations ≤ X?

Step 2: Why this is tricky
Unlike previous examples, the feasibility is not a simple sum — we have to check per-gap:
For each gap between stations:
gap = stations[i+1] - stations[i]
We can add extra stations to split it
Number of extra stations needed = ceil(gap / X) - 1
Then sum all needed stations across all gaps
Check if ≤ K
Notice: this is greedy in a subtle way, but the overall answer-space search is still binary search.

Step 3: Monotonicity
Why is f(X) monotonic?
If f(X) is true (max distance ≤ X with ≤ K extra stations),
Then f(Y) is also true for any Y > X (because fewer stations are needed, and constraint is looser).
This is the key insight interviewers want you to verbalize.

Step 4 Check understanding verbally
Answer this:
Why do we compute ceil(gap / X) - 1 for each gap instead of just counting gaps or dividing by K?
This is subtle — the interviewer wants you to justify why this greedy per-gap calculation works.


Step 5 : Why this is tricky feasibility
The feasibility check is per-gap, not total sum
Each gap can require a different number of stations
Candidate distance X is a float, not integer
Monotonicity still holds: if X works, any larger X also works

Step 6 : Summary
“We binary search over the maximum allowed distance X.
For each candidate X, we check feasibility by counting how many stations are needed in each gap to make all segments ≤ X.
If total ≤ K, it's feasible, and we shrink X; otherwise we increase X.
The function is monotonic because larger X relaxes constraints.”
'''

import math

def can_place(stations, K, max_dist):
    # Count how many stations are needed to ensure no gap exceeds max_dist
    required = 0
    for i in range(len(stations) - 1):
        gap = stations[i+1] - stations[i]
        # How many stations needed in this gap?
        required += math.floor(gap / max_dist)
    return required <= K

class Solution:
    def minmaxGasDist(self, stations: List[int], K: int) -> float:
        left = 0.0
        right = stations[-1] - stations[0]  # max possible gap
        eps = 1e-6  # precision threshold

        while right - left > eps:
            mid = (left + right) / 2
            if can_place(stations, K, mid):
                right = mid  # try smaller max distance
            else:
                left = mid  # need larger distance

        return left  # or right, both within eps
