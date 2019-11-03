class Vertex:
    def __init__(self, normal: [], x: int, y: int, z: int):
        self.Normal = normal
        self.X = x
        self.Y = y
        self.Z = z


def _read_byte(file):
    res = []
    for i in range(4):
        temp = hex(ord(file.read(1)))[2:]
        if temp == "0":
            temp = "00"
        res.append(temp)
    return _get_dec_from_bytes(res)


def _get_dec_from_bytes(bytes: []):
    res = ""
    for i in range(3, -1, -1):
        res += bytes[i]
    return int(res, 16)


def _read_count_facets(file):
    file.seek(80)
    return _read_byte(file)


def _read_normal(file):
    res = []
    for i in range(3):
        res.append(_read_byte(file))
    return res


def _read_vertexes_triangle(file):
    res = []
    for vert in range(0, 3):
        vertex = []
        for node in range(0, 3):
            vertex.append(_read_byte(file))
        res.append(vertex)
    file.seek(2)
    return res


def _open_file(path: str):
    return open(path, "rb")


def _close_file(file):
    file.close()


def read_stl(path: str):
    file = _open_file(path)
    count_triangles = _read_count_facets(file)
    res = []
    for i in range(count_triangles):
        normal = _read_normal(file)
        triangle = _read_vertexes_triangle(file)
        vertex = Vertex(normal, *triangle)
        res.append(vertex)
    _close_file(file)
    return res


#test = read_stl("cube1.stl")
#qwe