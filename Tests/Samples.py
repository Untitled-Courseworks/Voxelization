import math
from OcTree.NodeOcTree import Node


def cube():
    # TODO ошибка в мешах
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


def pyramid():
    """
    Пример простой пирамиды с треугольным основанием
    :return: Список меши пирамиды с треугольным основанием
    """
    return [[[0, 0, 3], [0, 0, 0], [0, 3, 0], [0, -9, 0]],
            [[0, 0, 3], [0, 0, 0], [3, 0, 0], [9, 0, 0]],
            [[0, 0, 3], [0, 3, 0], [3, 0, 0], [0, 9, 9]],
            [[3, 0, 0], [0, 0, 0], [0, 3, 0], [-9, 0, 9]]]


def pyramid1():
    """
    Пример простой пирамиды с треугольным основанием
    :return: Список меши пирамиды с треугольным основанием
    """
    return [[[0, 0, 3], [0, 0, 0], [0, 3, 0]],
            [[0, 0, 3], [0, 0, 0], [3, 0, 0]],
            [[0, 0, 3], [0, 3, 0], [3, 0, 0]],
            [[3, 0, 0], [0, 0, 0], [0, 3, 0]]]


def triangle():
    """
    Пример треугольника на плоскости OX
    :return:
    """
    return [
        [[0, 0, 0], [0, 3, 0], [3, 3, 0], []]
    ]


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
            _compare(min, max, v[0], i)
            _compare(min, max, v[1], i)
            _compare(min, max, v[2], i)

    return [max[i] - min[i] for i in range(3)]


def _compare(min: [], max: [], vertex: [], i: int):
    if min[i] > vertex[i]:
        min[i] = vertex[i]
    if max[i] < vertex[i]:
        max[i] = vertex[i]


def get_empty_node_with_empty_children(size=1.0):
    res = Node(None, size, [0, 0, 0], [])
    res.add_children()
    return res

