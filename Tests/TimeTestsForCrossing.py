import time
import Crossing
from sympy import Line, Point, Segment


start_time = time.time()
for i in range(1000):
    a = Crossing._check_crossing_lines([0, 0], [2, 0], [0, 2], [2, 2])
print(a)
for i in range(1000):
    a = Crossing._check_crossing_lines([0, 0], [2, 2], [0, 2], [2, 0])
print(a)
print(print("--- %s seconds ---" % (time.time() - start_time)))


def crossing(p1: Point, p2: Point, p3: Point, p4: Point):
    line1, seg1 = Line(p1, p2), Segment(p1, p2)
    line2, seg2 = Line(p3, p4), Segment(p3, p4)
    intersect = line1.intersection(line2)
    if intersect:
        seg1 = Segment(p1, p2)
        seg2 = Segment(p3, p4)
        pi = intersect[0]
        return seg1.contains(pi) and seg2.contains(pi)


start_time = time.time()
for i in range(1000):
    a = crossing(Point(0, 0), Point(2, 0), Point(0, 2), Point(2, 2))
print(a)
for i in range(1000):
    a = crossing(Point(0, 0), Point(2, 2), Point(0, 2), Point(2, 0))
print(a)
print(print("--- %s seconds ---" % (time.time() - start_time)))
