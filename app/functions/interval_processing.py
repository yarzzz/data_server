from typing import List
from collections import defaultdict

def is_intersecting(interval1, interval2):
    a1, b1 = interval1
    a2, b2 = interval2
    return b1 >= a2 and b2 >= a1

def check_all(intervals, ids) -> bool:
    print(ids)
    n = len(intervals)
    for i in range(n):
        for j in range(i + 1, n):
            if is_intersecting(intervals[i], intervals[j]):
                if not (ids[intervals[i]] & ids[intervals[j]]):
                    return False
            else:
                if ids[intervals[i]] & ids[intervals[j]]:
                    return False
    return True

def assign_ids(intervals):
    n = len(intervals)
    letters = "abcdefghijklmnopqrstuvwxyz"
    cur = 0

    ids = defaultdict(set)
    
    all_points = sorted(list({x[0] for x in intervals} ^ {x[1] for x in intervals}))
    left = defaultdict(set)
    right = defaultdict(set)
    for interval in intervals:
        left[interval[0]].add(interval)
        right[interval[1]].add(interval)
    cur_intervals = set()
    new_left = False

    for point in all_points:
        if left[point]:
            cur_intervals ^= left[point]
            new_left = True
        if right[point]:
            if new_left:
                for x in cur_intervals:
                    ids[x].add(letters[cur])
            cur += 1
            cur_intervals -= right[point]
            new_left = False
            
    return ids

async def process_intervals(combined_data: List[List[List[object]]]) -> str:
    data = combined_data[0]

    # 根据传入的列名过滤数据
    intervals = []
    for x, y in zip(data[0], data[1]):
        intervals.append((x, y))

    assigned_ids = assign_ids(intervals)

    result = ""
    for interval in intervals:
        result += f"Interval: {interval}, IDs: {''.join(sorted(assigned_ids[interval]))}<br>"
    
    return result
