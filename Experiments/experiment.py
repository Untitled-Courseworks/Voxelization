import matplotlib.pyplot as plt
from sympy import Line, Point, Segment
import numpy as np


def crossing(p1: Point, p2: Point, p3: Point, p4: Point):
    line1, seg1 = Line(p1, p2), Segment(p1, p2)
    line2, seg2 = Line(p3, p4), Segment(p3, p4)
    intersect = line1.intersection(line2)
    if intersect:
        seg1 = Segment(p1, p2)
        seg2 = Segment(p3, p4)
        pi = intersect[0]
        return seg1.contains(pi) and seg2.contains(pi)


print(crossing(Point(0, 1), Point(2, 0), Point(0, 4), Point(2, 0)))

x1, y1 = [0, 1], [-1, 0]
x2, y2 = [0, 4], [2, 0]

# объекты точек
p1, p2, p3, p4 = (Point(x1[0], y1[0]), Point(x1[1], y1[1]),
                  Point(x2[0], y2[0]), Point(x2[1], y2[1]))

# объекты прямых для установления факта пересечения
# объекты отрезков для проверки наличия точки пересечения уже на отрезке
line1, seg1 = Line(p1, p2), Segment(p1, p2)
line2, seg2 = Line(p3, p4), Segment(p3, p4)

intersect = line1.intersection(line2)
print(intersect)

l1, = plt.plot(x1, y1, marker='o', zorder=3)
l2, = plt.plot(x2, y2, marker='o', zorder=3)

if intersect:
    pi = intersect[0]
    if not seg1.contains(pi):
        xydata = l1.get_xydata()
        xydata = np.vstack((xydata, [pi.x, pi.y]))
        plt.plot(xydata[:, 0], xydata[:, 1], '--', alpha=.5)

    if not seg2.contains(pi):
        xydata = l2.get_xydata()
        xydata = np.vstack((xydata, [pi.x, pi.y]))
        plt.plot(xydata[:, 0], xydata[:, 1], '--', alpha=.5)
plt.show()