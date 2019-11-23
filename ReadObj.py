import math


def read_file(path: str):
    """
    парсит файл на меши
    :param path: путь к файлу
    :return:
    """
    mod = _get_vertexes(path)
    vertexes = mod[0]
    result = []
    with open(path, "r") as file:
        for line in file:
            line = line.strip().split()
            if len(line) > 0 and line[0].lower() == "f":
                line = [int(i.split("/")[0]) for i in line[1:]]
                result.append([vertexes[i - 1] for i in line])
    return result, mod[1]


def _get_vertexes(path: str):
    result = []
    min_x = math.inf
    min_y = math.inf
    min_z = math.inf
    max_x = 0.0
    max_y = 0.0
    max_z = 0.0
    with open(path) as file:
        for line in file:
            line = line.strip().split()
            if len(line) > 0 and line[0].lower() == "v":
                line = [float(i) for i in line[1:]]
                result.append(line)
                if min_x > line[0]:
                    min_x = line[0]
                if max_x < line[0]:
                    max_x = line[0]

                if min_y > line[1]:
                    min_y = line[1]
                if max_y < line[1]:
                    max_y = line[1]

                if min_z > line[2]:
                    min_z = line[2]
                if max_z < line[2]:
                    max_z = line[2]
    return result, [[min_x, max_x], [min_y, max_y], [min_z, max_z]]


def _check_line(line: str, letter: str):
    line = line.strip().split()
    return len(line) > 0 and line[0].lower() == letter
