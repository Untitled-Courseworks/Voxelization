import math
import numpy as np


class Mesh:
    def __init__(self, normal: [], v1: [], v2: [], v3: []):
        self.Normal = normal
        self.V1 = v1
        self.V2 = v2
        self.V3 = v3


size = 0.5


def return_sample():
    """
    Пример простой пирамиды с треугольным основанием
    :return: Список меши пирамиды с треугольным основанием
    """
    return [Mesh([0, -9, 0], [0, 0, 3], [0, 0, 0], [3, 0, 3]),
            Mesh([9, 0, 0], [0, 0, 3], [0, 0, 0], [0, 3, 0]),
            Mesh([0, 9, 9], [0, 0, 3], [3, 0, 3], [0, 3, 0]),
            Mesh([-9, 0, 9], [0, 0, 0], [3, 0, 3], [0, 3, 0])]


def find_size_model(model: []):
    """
    Рассчитывает размеры модели по крайним точкам
    :param model: Меши модели
    :return: возвращает размеры в формате [x, y, z]
    """
    min = [math.inf, math.inf, math.inf]
    max = [0, 0, 0]

    for v in model:
        for i in range(3):
            compare(min, max, v.V1, i)
            compare(min, max, v.V2, i)
            compare(min, max, v.V3, i)

    return [max[i] - min[i] for i in range(3)]


def compare(min: [], max: [], vertex: [], i: int):
    if min[i] > vertex[i]:
        min[i] = vertex[i]
    if max[i] < vertex[i]:
        max[i] = vertex[i]


model = return_sample()
size_mod = find_size_model(model)
test = np.array(([[], []], [[], []], [[], []]))
