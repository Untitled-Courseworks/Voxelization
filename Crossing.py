def crossing(mesh: [], voxel: [], size_voxel: float):
    """
    Проверка, что у меша и вокселя есть общие точки
    :param mesh: меш
    :param voxel: координаты одной вершины вокселя
    :param size_voxel: размер вокселя
    :return: True, если есть общее количество точек и False - в противном случае
    """
    # TODO
    #   Предусмотреть, что меш может быть не только треугольной формы
    #   Написать метод, определяюший принадлежность точки к многоугольнику
    mesh_projections = _get_all_projections(mesh, 3)
    voxel_projections = _get_all_projections([voxel], 1)
    for i in range(3):
        if not _check_all(mesh_projections[i], voxel_projections[i][0], size_voxel):
            return False
    return True


def _get_all_projections(vertices: [], count_vertices: int):
    """
    Проецирует точки на три плоскости: XY, XZ, YZ
    Принимает данные в формате [[x, y, z], [x, y, z], ...]
    :param vertices: вершины
    :param count_vertices: количество вершин, которые надо спроецировать
    :return: список с проекциями в формате [[[x, y], [x, y], ...], [[x, z], [x, z], ...], [[y, z], [y, z], ...]]
    """
    x_y = []
    x_z = []
    y_z = []
    for i in range(count_vertices):
        x_y.append([vertices[i][0], vertices[i][1]])
        x_z.append([vertices[i][0], vertices[i][2]])
        y_z.append([vertices[i][1], vertices[i][2]])
    return [x_y, x_z, y_z]


def _check_all(mesh_projection: [], voxel_projection: [], size_voxel: float):
    """
    Объединяет все проверки
    :param mesh_projection: проекция меша
    :param voxel_projection: проекция вокселя
    :param size_voxel: размер вокселя
    :return: True, если есть общие точки, False, во всех остальных случаях
    """
    if _check_mesh_in_voxel(mesh_projection, voxel_projection, size_voxel):
        return True
    if _check_voxel_in_mesh(mesh_projection, voxel_projection, size_voxel):
        return True
    if _check_crossing_projections(voxel_projection, size_voxel, mesh_projection):
        return True
    return False


def _check_mesh_in_voxel(mesh_projection: [], voxel_projection: [], size_voxel: float):
    """
    Проверяет включение меша в вкосель
    :param mesh_projection: проекция меша
    :param voxel_projection: координата проекции вокселя
    :param size_voxel: размер вокселя
    :return: True, если включает в себя, False, если нет
    """
    # TODO Меш не только треугольный
    return _point_in_square(voxel_projection, size_voxel, mesh_projection[0]) or \
           _point_in_square(voxel_projection, size_voxel, mesh_projection[1]) or \
           _point_in_square(voxel_projection, size_voxel, mesh_projection[2])


def _point_in_square(square: [], size_square: float, point: []):
    return square[0] <= point[0] <= square[0] + size_square and square[1] <= point[1] <= square[1] + size_square


def _check_voxel_in_mesh(mesh_projection: [], voxel_projection: [], size_voxel: float):
    """
    Проверяет включение вокселя в меш
    :param mesh_projection: проекция меша
    :param voxel_projection: проекция вокселя
    :param size_voxel: размер вокселя
    :return: True, если включает в себя, False, если нет
    """
    return _point_in_triangle(voxel_projection, mesh_projection) or \
           _point_in_triangle([voxel_projection[0], voxel_projection[1] + size_voxel], mesh_projection) or \
           _point_in_triangle([voxel_projection[0] + size_voxel, voxel_projection[1]], mesh_projection) or \
           _point_in_triangle([voxel_projection[0] + size_voxel, voxel_projection[1] + size_voxel], mesh_projection)


def _point_in_triangle(point: [], triangle: []):
    a = _det(triangle[0], triangle[1], point)
    b = _det(triangle[1], triangle[2], point)
    c = _det(triangle[2], triangle[0], point)

    return (a <= 0 and b <= 0 and c <= 0) or (a > 0 and b > 0 and c > 0)


def _det(p_1: [], p_2: [], p_3: []):
    return (p_1[0] - p_3[0]) * (p_2[1] - p_1[1]) - (p_2[0] - p_1[0]) * (p_1[1] - p_3[1])


def _check_crossing_projections(voxel_projection: [], size_voxel: float, mesh_projections: []):
    """
    Проверяет пересечение проекции вокселя и проекции меша
    :param voxel_projection: проекция вокселя
    :param size_voxel: размер вокселя
    :param mesh_projections: проекция меша
    :return: True, если есть пересечение, False, во всех остальных случаях
    """
    for i in range(len(mesh_projections)):
        if i + 1 == len(mesh_projections):
            return _check_crossing_projection_and_line(voxel_projection, size_voxel, mesh_projections[i],
                                                       mesh_projections[0])
        else:
            if _check_crossing_projection_and_line(voxel_projection, size_voxel, mesh_projections[i],
                                                   mesh_projections[i + 1]):
                return True
    return False


def _check_crossing_projection_and_line(voxel_projection: [], size_voxel: float, ver_1: [], ver_2: []):
    """
    Проверяет пересечение проекции вокселя с линией проекции меша
    :param voxel_projection: координаты верхней левой вершины проекции вокселя
    :param size_voxel: размер вокселя
    :param ver_1: первая вершина
    :param ver_2: вторая вершина
    :return:
    """
    if _check_crossing_lines(ver_1, ver_2, voxel_projection, [voxel_projection[0], voxel_projection[1] + size_voxel]):
        return True
    elif _check_crossing_lines(ver_1, ver_2, voxel_projection, [voxel_projection[0] + size_voxel, voxel_projection[1]]):
        return True
    elif _check_crossing_lines(ver_1, ver_2, [voxel_projection[0], voxel_projection[1] + size_voxel],
                               [voxel_projection[0] + size_voxel, voxel_projection[1] + size_voxel]):
        return True

    elif _check_crossing_lines(ver_1, ver_2, [voxel_projection[0] + size_voxel, voxel_projection[1]],
                               [voxel_projection[0] + size_voxel, voxel_projection[1] + size_voxel]):
        return True
    return False


def _check_crossing_lines(ver_1: [], ver_2: [], voxel_1: [], voxel_2: []):
    """
    Проверяет, пересекаются ли линия грани проекции вокселя и линия грани проекции
     меша и находится ли точка пересечения между вершинами проекции вокселя
    :param ver_1: Первая вершина проекции грани меша
    :param ver_2: вторая вершина проекции грани меша
    :param voxel_1: первая вершина проекции грани вокселя
    :param voxel_2: вторая вершина проекции грани вокселя
    :return: True, если есть пересечение и точка пересечения лежит между вершинами проекции грани вокселя,
    False, в остальных случаях
    """
    devider = _det_([ver_1[0] - ver_2[0], ver_1[1] - ver_2[1]], [voxel_1[0] - voxel_2[0], voxel_1[1] - voxel_2[1]])
    if devider == 0:
        a1 = ver_1[1] - ver_2[1]
        b1 = ver_2[0] - ver_1[0]
        c1 = ver_1[0] * ver_2[1] - ver_2[0] * ver_1[1]
        a2 = voxel_1[1] - voxel_2[1]
        b2 = voxel_2[0] - voxel_1[0]
        c2 = voxel_1[0] * voxel_2[1] - voxel_2[0] * voxel_1[1]
        if _det_([a1, b1], [a2, b2]) == 0 and _det_([a1, c1], [a2, c2]) == 0 and _det_([b1, c1], [b2, c2]) == 0:
            return voxel_1[0] <= ver_1[0] <= voxel_2[0] and voxel_1[1] <= ver_1[1] <= voxel_2[1] or \
                   voxel_1[0] <= ver_2[0] <= voxel_2[0] and voxel_1[1] <= ver_2[1] <= voxel_2[1]

        if _det_([a1, b1], [a2, b2]) == 0:
            return False

    x = (_det_(ver_1, ver_2) * (voxel_1[0] - voxel_2[0]) - (ver_1[0] - ver_2[0]) * _det_(voxel_1, voxel_2)) / devider
    y = (_det_(ver_1, ver_2) * (voxel_1[1] - voxel_2[1]) - (ver_1[1] - ver_2[1]) * _det_(voxel_1, voxel_2)) / devider

    return _point_between_two_points(voxel_1, voxel_2, [x, y]) and _point_between_two_points(ver_1, ver_2, [x, y])


def _point_between_two_points(p_1: [], p_2: [], cur_p: []):
    dxl = p_2[0] - p_1[0]
    dyl = p_2[1] - p_1[1]
    if abs(dxl) >= abs(dyl):
        if dxl > 0:
            return p_1[0] <= cur_p[0] <= p_2[0]
        return p_2[0] <= cur_p[0] <= p_1[0]
    else:
        if dyl > 0:
            return p_1[1] <= cur_p[1] <= p_2[1]
        return p_2[1] <= cur_p[1] <= p_1[1]


def _det_(ver_1: [], ver_2: []):
    return ver_1[0] * ver_2[1] - ver_2[0] * ver_1[1]
