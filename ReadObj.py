import math


def read_file(path: str):
    """
    Возвращает список мешей из файла по указаному пути
    :param path: путь к файлу
    :return: список в формате [[mesh], [mesh], ...], где [mesh] это [[v1], [v2], [v3]], где [v] это [x, y, z],
        [min_x, max_x], [min_y, max_y], [min_z, max_z]
    """
    res = []
    with open(path, "r") as file:
        points = _get_list_vertex(file)
        for string in file:
            temp = string.split()
            if temp[0] == "f":
                res.append([points[0][int(i)] for i in temp[1:]])

    return res, points[1], points[2], points[3]


def _get_list_vertex(file):
    points = []

    min_x = math.inf
    max_x = 0
    min_y = math.inf
    max_y = 0
    min_z = math.inf
    max_z = 0

    for string in file:
        temp = string.split()
        if temp[0].lower() == "v":
            points.append([float(i) for i in temp[1:]])
            if min_x > float(temp[1]):
                min_x = float(temp[1])
            if min_y > float(temp[2]):
                min_y = float(temp[2])
            if min_z > float(temp[3]):
                min_z = float(temp[3])

            if max_x < float(temp[1]):
                max_x = float(temp[1])
            if max_y < float(temp[2]):
                max_y = float(temp[2])
            if max_z < float(temp[3]):
                max_z = float(temp[3])

        if len(points) > 0 and temp[0].lower() != "v":
            break
    return points, [min_x, max_x], [min_y, max_y], [min_z, max_z]


test = read_file("Tests/test.obj")
print(len(test))
