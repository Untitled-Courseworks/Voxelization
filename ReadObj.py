def read_file(path: str):
    """
    парсит файл на меши
    :param path: путь к файлу
    :return:
    """
    vertexes = _get_vertexes(path)
    result = []
    with open(path, "r") as file:
        for line in file:
            line = line.strip().split()
            if len(line) > 0 and line[0].lower() == "f":
                line = [int(i.split("/")[0]) for i in line[1:]]
                result.append([vertexes[i - 1] for i in line])
    return result


def _get_vertexes(path: str):
    result = []
    with open(path) as file:
        for line in file:
            line = line.strip().split()
            if len(line) > 0 and line[0].lower() == "v":
                result.append([float(i) for i in line[1:]])
    return result


def _check_line(line: str, letter: str):
    line = line.strip().split()
    return len(line) > 0 and line[0].lower() == letter
