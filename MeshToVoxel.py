import math
from Crossing import crossing
import Visualization


class Mesh:
    # Временно
    def __init__(self, normal: [], v1: [], v2: [], v3: []):
        self.Normal = normal
        self.V1 = v1
        self.V2 = v2
        self.V3 = v3


def return_sample_pyramid():
    # Временно
    """
    Пример простой пирамиды с треугольным основанием
    :return: Список меши пирамиды с треугольным основанием
    """
    return [[[0, -9, 0], [0, 0, 3], [0, 0, 0], [3, 0, 3]],
            [[9, 0, 0], [0, 0, 3], [0, 0, 0], [0, 3, 0]],
            [[0, 9, 9], [0, 0, 3], [3, 0, 3], [0, 3, 0]],
            [[-9, 0, 9], [0, 0, 0], [3, 0, 3], [0, 3, 0]]]


def return_sample_cube():
    # Временно
    """
    Пример куба с длиной граней 3
    :return: Список мешей куба
    """
    return [
        [[0, 3, 3], [3, 3, 3], [3, 0, 3], []],
        [[0, 3, 3], [0, 0, 3], [3, 0, 3], []],

        [[0, 3, 3], [0, 0, 3], [0, 0, 0], []],
        [[0, 3, 3], [0, 3, 0], [0, 0, 0], []],

        [[0, 3, 3], [3, 3, 3], [0, 3, 0], []],
        [[0, 3, 3], [3, 3, 0], [0, 3, 0], []],

        [[3, 0, 3], [0, 0, 3], [3, 3, 3], []],
        [[3, 0, 3], [3, 0, 0], [3, 3, 3], []],

        [[3, 3, 3], [3, 0, 3], [3, 0, 0], []],
        [[3, 3, 3], [3, 3, 0], [3, 0, 0], []],

        [[0, 3, 0], [3, 3, 0], [3, 0, 0], []],
        [[0, 3, 0], [0, 0, 0], [3, 0, 0], []],
    ]


def find_size_model(model: []):
    # Временно
    """
    Рассчитывает размеры модели по крайним точкам
    :param model: Меши модели
    :return: возвращает размеры в формате [x, y, z]
    """
    min = [math.inf, math.inf, math.inf]
    max = [0, 0, 0]

    for v in model:
        for i in range(3):
            compare(min, max, v[0], i)
            compare(min, max, v[1], i)
            compare(min, max, v[2], i)

    return [max[i] - min[i] for i in range(3)]


def compare(min: [], max: [], vertex: [], i: int):
    # Временно
    if min[i] > vertex[i]:
        min[i] = vertex[i]
    if max[i] < vertex[i]:
        max[i] = vertex[i]


def get_voxel_model(model, size_mod):
    res = []
    for z in range(math.ceil(size_mod[2] / size)):
        for y in range(math.ceil(size_mod[1] / size)):
            for x in range(math.ceil(size_mod[0] / size)):
                for m in model:
                    if crossing(m, [x, y, z], size):
                        res.append([x, y, z])
    return res


# Временно
size = 1
model = return_sample_cube()
size_mod = find_size_model(model)
voxels = get_voxel_model(model, size_mod)
print(len(voxels))
Visualization.get_model(voxels)
print(len(voxels))

# print(check_crossing_lines([2, 0], [4, 0], [1, 0], [3, 0]))
