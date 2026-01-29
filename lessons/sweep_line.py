'''
The sweep line algorithm processes events (like the start or end of an interval) 
in sorted order along a line, updating some data structure as it moves 
to efficiently solve problems involving intervals or geometric shapes.

General Notes on the Generic Sweep Line Algorithm:
- Sorting Events: Sorting is key in the sweep line algorithm. 
It ensures that events are processed in the correct order.
- State Updates: You track the state (like active count, set of active intervals, etc.) during the sweep. 
This can vary depending on the problem.
- Handling Event Types: The event types (e.g., 'start', 'end') and 
how you process them will depend on the specific problem you're solving.

Time and Space Complexity:
- Time Complexity: O(n log n) — Sorting the events takes O(n log n), 
where n is the number of events. Processing the events is linear O(n).
- Space Complexity: O(n) — We store the events and potentially additional state information.

Applications of Sweep Line:
The sweep line algorithm is widely used for:
- Interval problems (counting overlaps, finding maximum coverage).
- Geometric problems (e.g., computing the union of rectangles, finding intersections of line segments).
- Event-driven simulations where the events are processed in an ordered fashion, 
like line segment intersection problems, or range queries.

Generic Sweep Line Algorithm Implementation

Events: Each "event" could be something like the start or end of an interval, 
or any other event where you need to update a state.

Sorting: Events are sorted primarily by their position.

Processing Events: As you process each event, you update some state 
(e.g., current count, active set, or coverage) accordingly.
'''
from collections import defaultdict

def sweep_line(events):
    # Step 1: Sort events primarily by position
    # If two events have the same position, we process 'start' events before 'end' events
    events.sort(key=lambda x: (x[0], x[1] == 'end'))
    
    # Step 2: Initialize a state to track (e.g., a counter, or active set)
    active_count = 0  # For example, we count how many events are "active" at each position
    
    # Step 3: Process events and update state
    result = []
    for event in events:
        position, event_type = event
        
        # Update the state depending on the type of the event
        if event_type == 'start':
            active_count += 1
        elif event_type == 'end':
            active_count -= 1
        
        # Collect results (or just update state, depending on the problem)
        result.append((position, active_count))
    
    return result
