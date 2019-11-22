import math
#Временно
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
    return [Mesh([0, -9, 0], [0, 0, 3], [0, 0, 0], [3, 0, 3]),
            Mesh([9, 0, 0], [0, 0, 3], [0, 0, 0], [0, 3, 0]),
            Mesh([0, 9, 9], [0, 0, 3], [3, 0, 3], [0, 3, 0]),
            Mesh([-9, 0, 9], [0, 0, 0], [3, 0, 3], [0, 3, 0])]


def return_sample_cube():
    # Временно
    """
    Пример куба с длиной граней 3
    :return: Список мешей куба
    """
    return [
        Mesh([], [0, 3, 3], [3, 3, 3], [3, 0, 3]),
        Mesh([], [0, 3, 3], [0, 0, 3], [3, 0, 3]),

        Mesh([], [0, 3, 3], [0, 0, 3], [0, 0, 0]),
        Mesh([], [0, 3, 3], [0, 3, 0], [0, 0, 0]),

        Mesh([], [0, 3, 3], [3, 3, 3], [0, 3, 0]),
        Mesh([], [0, 3, 3], [3, 3, 0], [0, 3, 0]),

        Mesh([], [3, 0, 3], [0, 0, 3], [3, 3, 3]),
        Mesh([], [3, 0, 3], [3, 0, 0], [3, 3, 3]),

        Mesh([], [3, 3, 3], [3, 0, 3], [3, 0, 0]),
        Mesh([], [3, 3, 3], [3, 3, 0], [3, 0, 0]),

        Mesh([], [0, 3, 0], [3, 3, 0], [3, 0, 0]),
        Mesh([], [0, 3, 0], [0, 0, 0], [3, 0, 0]),
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
            compare(min, max, v.V1, i)
            compare(min, max, v.V2, i)
            compare(min, max, v.V3, i)

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
                if is_voxel([x, y, z], model, size):
                    res.append([x, y, z])
    return res


def is_voxel(voxel: [], model: [], size_voxel: float):
    for mesh in model:
        if check_all_projection(voxel, size_voxel, mesh.V1, mesh.V2):
            return True
        elif check_all_projection(voxel, size_voxel, mesh.V1, mesh.V3):
            return True
        elif check_all_projection(voxel, size_voxel, mesh.V2, mesh.V3):
            return True
    return False


def check_all_projection(voxel: [], size_voxel: float, ver_1: [], ver_2: []):
    # TODO
    #  Нет проверки, когда меш полностью внутри проекции
    #  Нет проверки, когда воксель полностью внутри меша
    return check_crossing_projection([voxel[0], voxel[1]], size_voxel, ver_1, ver_2) and \
           check_crossing_projection([voxel[1], voxel[2]], size_voxel, ver_1, ver_2) and \
           check_crossing_projection([voxel[0], voxel[2]], size_voxel, ver_1, ver_2)


def check_crossing_projection(voxel_projection: [], size_voxel: float, ver_1: [], ver_2: []):
    """
    Проверяет пересечение проекции вокселя с линией проекции меша
    :param voxel_projection: координаты верхней левой вершины проекции вокселя
    :param size_voxel: размер вокселя
    :param ver_1: первая вершина
    :param ver_2: вторая вершина
    :return:
    """
    if check_crossing_lines(ver_1, ver_2, voxel_projection, [voxel_projection[0], voxel_projection[1] + size_voxel]):
        return True
    elif check_crossing_lines(ver_1, ver_2, voxel_projection, [voxel_projection[0] + size_voxel, voxel_projection[1]]):
        return True
    elif check_crossing_lines(ver_1, ver_2, [voxel_projection[0], voxel_projection[1] + size_voxel],\
            [voxel_projection[0] + size_voxel, voxel_projection[1] + size_voxel]):
        return True

    elif check_crossing_lines(ver_1, ver_2, [voxel_projection[0] + size_voxel, voxel_projection[1]],\
            [voxel_projection[0] + size_voxel, voxel_projection[1] + size_voxel]):
        return True
    return False


def check_crossing_lines(ver_1: [], ver_2: [], voxel_1: [], voxel_2: []):
    """
    Проверяет, пересекаются ли две линии и находится ли точка пересечения между вершинами вокселя
    :param ver_1: Первая вершина меша
    :param ver_2: вторая вершина меша
    :param voxel_1: первая вершина вокселя
    :param voxel_2: вторая вершина вокселя
    :return:
    """
    devider = det([ver_1[0] - ver_2[0], ver_1[1] - ver_2[1]], [voxel_1[0] - voxel_2[0], voxel_1[1] - voxel_2[1]])
    if devider == 0:
        a1 = ver_1[1] - ver_2[1]
        b1 = ver_2[0] - ver_1[0]
        c1 = ver_1[0] * ver_2[1] - ver_2[0] * ver_1[1]
        a2 = voxel_1[1] - voxel_2[1]
        b2 = voxel_2[0] - voxel_1[0]
        c2 = voxel_1[0] * voxel_2[1] - voxel_2[0] * voxel_1[1]
        if det([a1, b1], [a2, b2]) == 0 and det([a1, c1], [a2, c2]) == 0 and det([b1, c1], [b2, c2]) == 0:
            return voxel_1[0] <= ver_1[0] <= voxel_2[0] and voxel_1[1] <= ver_1[1] <= voxel_2[1] or \
                   voxel_1[0] <= ver_2[0] <= voxel_2[0] and voxel_1[1] <= ver_2[1] <= voxel_2[1]

        if det([a1, b1], [a2, b2]) == 0:
            return False

    x = (det(ver_1, ver_2) * (voxel_1[0] - voxel_2[0]) - (ver_1[0] - ver_2[0]) * det(voxel_1, voxel_2)) / devider
    y = (det(ver_1, ver_2) * (voxel_1[1] - voxel_2[1]) - (ver_1[1] - ver_2[1]) * det(voxel_1, voxel_2)) / devider

    return voxel_1[0] <= x <= voxel_2[0] and voxel_1[1] <= y <= voxel_2[1]


def det(ver_1: [], ver_2: []):
    return ver_1[0] * ver_2[1] - ver_2[0] * ver_1[1]


# Временно
size = 1
model = return_sample_cube()
size_mod = find_size_model(model)
voxels = get_voxel_model(model, size_mod)
#Visualization.get_model(voxels)
#print(len(voxels))

#print(check_crossing_lines([2, 0], [4, 0], [1, 0], [3, 0]))

print(input(60))