def crossing(voxel: [], size_voxel: float, mesh: []):
    crossing_points = _get_list_crossing_points(voxel, size_voxel, mesh)
    if crossing_points is None:
        #TODO
        pass
    crossing_points = _get_all_projections(crossing_points, len(crossing_points))
    mesh_projections = _get_all_projections(mesh, len(mesh) - 1)
    for i in range(3):
        for point in crossing_points[i]:
            if not _point_in_triangle(point, mesh_projections[i]):
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


def _point_in_triangle(point: [], triangle: []):
    """
    Проверяет, принадлежат ли точка треугольнику на плоскости
    :param point: Проверяемая точка
    :param triangle: треугольник на плоскости
    :return: True, усли принадлежит и False, если нет
    """
    a = _det(triangle[0], triangle[1], point)
    b = _det(triangle[1], triangle[2], point)
    c = _det(triangle[2], triangle[0], point)

    return (a <= 0 and b <= 0 and c <= 0) or (a > 0 and b > 0 and c > 0)


def _det(p_1: [], p_2: [], p_3: []):
    return (p_1[0] - p_3[0]) * (p_2[1] - p_1[1]) - (p_2[0] - p_1[0]) * (p_1[1] - p_3[1])


def _get_list_crossing_points(voxel: [], size_voxel: float, mesh: []):
    """
    Составляет список точек пересечений плоскости меша и ребер вокселя
    :param voxel: точка вокселя
    :param size_voxel: размер ребра вокселя
    :param mesh: коодинаты меша
    :return: список точек пересечения в формате [[x, y, z], [x, y, z], ...]. Может быть от 0 до 6 или None,
    если меш представляет собой линию
    """
    all_edges_voxel = _get_all_edges(voxel, size_voxel)
    coefficients = _get_coefficients_plane(mesh[0], mesh[1], mesh[2])
    if coefficients == [0, 0, 0, 0]:
        return None
    res = []
    for edge in all_edges_voxel:
        temp = _get_crossing_point(edge[0], edge[1], coefficients)
        if temp is not None:
            res.append(temp)
    return res


def _get_all_edges(point: [], size_edge: float):
    p = _get_all_points(point, size_edge)
    return [
        [p[0], p[1]],
        [p[0], p[2]],
        [p[0], p[4]],
        [p[1], p[3]],
        [p[1], p[5]],
        [p[2], p[3]],
        [p[2], p[6]],
        [p[3], p[7]],
        [p[4], p[5]],
        [p[4], p[6]],
        [p[5], p[7]],
        [p[6], p[7]]
            ]


def _get_all_points(point: [], size_edge: float):
    """
    Возвращает все точки вокселя
    :param point:
    :param size_edge:
    :return:
    """
    res = []
    for z in range(2):
        for y in range(2):
            for x in range(2):
                res.append([x * size_edge + point[0], y * size_edge + point[1], z * size_edge + point[2]])
    return res


def _get_coefficients_plane(p1: [], p2: [], p3: []):
    """
    Возвращает коэффициенты уравнения плоскости меша
    :param p1:
    :param p2:
    :param p3:
    :return:
    """
    a = _calculate_coefficient([p1[1], p2[1], p3[1]], [p1[2], p2[2], p3[2]])
    b = - _calculate_coefficient([p1[0], p2[0], p3[0]], [p1[2], p2[2], p3[2]])
    c = _calculate_coefficient([p1[0], p2[0], p3[0]], [p1[1], p2[1], p3[1]])
    d = - a * p1[0] - b * p1[1] - c * p1[2]
    return [a, b, c, d]


def _calculate_coefficient(k1: [], k2: []):
    return (k1[1] - k1[0]) * (k2[2] - k2[1]) - (k2[1] - k2[0]) * (k1[2] - k1[1])


def _get_crossing_point(p1: [], p2: [], plane: []):
    """
    Возвращает точку пересечения между ллинией и плоскостью
    :param p1: первая точка
    :param p2: вторая точка
    :param plane: коэффициенты плоскости
    :return: точку пересечения, если прямая пересекает плоскость, первую точку, если совпадает, и None, если параллельна
    """
    if (p2[0] - p1[0]) * plane[0] + (p2[1] - p1[1]) * plane[1] + (p2[2] - p1[2]) * plane[2] != 0:
        param = _get_parameter(p1, p2, plane)
        return [(p2[i] - p1[i]) * param + p1[i] for i in range(3)]

    if p1[0] * plane[0] + p1[1] * plane[1] + p1[2] * plane[2] != 0:
        return p1

    return None


def _get_parameter(p1: [], p2: [], plane: []):
    return - (plane[0] * p1[0] + plane[1] * p1[1] + plane[2] * p1[2] + plane[3]) / \
        (plane[0] * (p2[0] - p1[0]) + plane[1] * (p2[1] - p1[1]) + plane[2] * (p2[2] - p1[2]))


def _check_crossing_segment(ver_1: [], ver_2: [], voxel_1: [], voxel_2: []):
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
    pass


def direction(p1: float, p2: float, p3: float):
    # TODO р1 - р3 - не координаты, а тычки с координатами
    return (p3 - p1) * (p2 - p1)

