#List
print("list->like vector")
lst = [1, 2, 3]
print(lst)

lst.append(4)      # push_back
print(lst)

lst.pop()          # pop_back
print(lst)

lst.insert(1, 99)  # insert at ith position o indexed
print(lst)

lst.remove(2)      # erase (first occurrence)
print(lst)

#Set
print("set->like unordered set")
s = {1, 2, 3}
print(s)
s.add(4)
print(s)
s.remove(2)
print(s)
if 3 in s: print("found")

print("tuple ->read code for unpacking")
tup = (1, 2, 3)
x, y, z = tup   # unpacking


print ("dict->like unordered map")
d = {"a": 1, "b": 2}
print(d)
d["c"] = 3        # insert
print(d["a"])     # access
d.pop("b")        # erase
for k, v in d.items(): print(k, v)

print("deque from collections->like queue")
from collections import deque
dq = deque([1, 2, 3])
print(dq)
dq.appendleft(0)   # push_front
print(dq)
dq.popleft()       # pop_front
print(dq)

print("heap-> like priority queue")
import heapq
arr = [3, 1, 4]
print(f"simeple array->{arr}")
heapq.heapify(arr)       # O(n)
print(f"after conversion to heap->{arr}")
heapq.heappush(arr, 0)   # push
print(arr)
print(heapq.heappop(arr)) # pop smallest
print(f"heap afer popping->{arr}")

