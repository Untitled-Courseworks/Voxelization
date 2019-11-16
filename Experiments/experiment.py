def in_polygon(x: float, y: float, xp: [], yp: []):
    c = 0
    for i in range(len(xp)):
        if ((yp[i] <= y <= yp[i - 1]) or (yp[i - 1] <= y <= yp[i])) and (x >= (xp[i - 1] - xp[i]) * (y - yp[i]) /
                                                                         (yp[i - 1] - yp[i]) + xp[i]):
            c = 1 - c
    return c


print(in_polygon(100, 0, (-100, 100, 100, -100), (100, 100, -100, -100)))
