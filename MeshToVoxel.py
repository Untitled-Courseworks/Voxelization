
import OcTree.CreateOcTree as Octree


def get_voxel_model(model, size_mod, size_voxel):
    """

    :param model:
    :param size_mod: [[min_x, max_x], [min_y, max_y], [min_z, max_z]]
    :param size_voxel:
    :return:
    """

    octree = Octree.get_octree(model, size_mod, size_voxel)

    res = []
    z = size_mod[2][0]
    while z <= size_mod[2][1]:
        y = size_mod[1][0]
        while y <= size_mod[1][1]:
            x = size_mod[0][0]
            while x <= size_mod[0][1]:
                if octree.check_crossing([x, y, z], size_voxel):
                    yield [x, y, z]
                    #res.append([x, y, z])
                    # TODO Временно
                    #print([x, y, z])
                x += size_voxel
            y += size_voxel
        z += size_voxel
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

