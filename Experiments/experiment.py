import matplotlib.pyplot as mp
import matplotlib.path as mpltPath
import numpy as np


def get_x_and_y(figure):
    res = [[], []]
    for i in range(len(figure)):
        res[0].append(figure[i][0])
        res[1].append(figure[i][1])
    return res


lenpoly = 100
polygon = [[np.sin(x)+0.5,np.cos(x)+0.5] for x in np.linspace(0,2*np.pi,lenpoly)[:-1]]

N = 10000
points = zip(np.random.random(N), np.random.random(N))

triangle = [[0.0, 0.0], [4.0, 0.0], [2.0, 4.0]]
#x_y = get_x_and_y(triangle)
path = mpltPath.Path(triangle)
inside2 = path.contains_points([[1, 2], [1, 1], [2, 0], [2, 1]])
for i in inside2:
    print(i)
print(inside2)
if inside2[1]:
    print(1)

