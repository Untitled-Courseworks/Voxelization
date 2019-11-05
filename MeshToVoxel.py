import math


class Mesh:
    def __init__(self, normal: [], v1: [], v2: [], v3: []):
        self.Normal = normal
        self.V1 = v1
        self.V2 = v2
        self.V3 = v3


def return_sample_pyramid():
    """
    Пример простой пирамиды с треугольным основанием
    :return: Список меши пирамиды с треугольным основанием
    """
    return [Mesh([0, -9, 0], [0, 0, 3], [0, 0, 0], [3, 0, 3]),
            Mesh([9, 0, 0], [0, 0, 3], [0, 0, 0], [0, 3, 0]),
            Mesh([0, 9, 9], [0, 0, 3], [3, 0, 3], [0, 3, 0]),
            Mesh([-9, 0, 9], [0, 0, 0], [3, 0, 3], [0, 3, 0])]

def return_sample_cube():
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


class voxel:
    def __init__(self, x: int, y: int, z: int, size: int, is_printed: bool):
        self.X = x
        self.Y = y
        self.Z = z
        self.Size = size
        self.Is_Printed = is_printed


def get_voxel_model(model: [], size_mod: []):
    """
    Крайне неэффективная реализация проверки на закрашивание вокселя
    :param model: Список мешей
    :param size_mod: Размеры модели
    :return: Список вокселей с параметром bool обозначающем его закрашивание. Координаты одноу вершины вокселя
    соостветствуют координатам его вызова в обратном порядке: voxels[z][y][x]
    """
    res = []
    z = 0
    while z < math.ceil(size_mod[2] / size):
        y = 0
        temp_y = []
        while y < math.ceil(size_mod[1] / size):
            x = 0
            temp_x = []
            while x < math.ceil(size_mod[0] / size):
                for v in model:
                    if check_intersection([x, y, z], size, [v.V1, v.V2, v.V3]):
                        #Использовал для отладки, можно посмотреть как находятся координаты
                        #temp_x.append([True, x, y, z])

                        temp_x.append(True)
                        break
                if len(temp_x) - 1 < x:
                    # Использовал для отладки, можно посмотреть как находятся координаты
                    #temp_x.append([False, x, y, z])

                    temp_x.append(False)
                x += 1
            temp_y.append(temp_x)
            y += 1
        res.append(temp_y)
        z += 1
    return res


def check_intersection(voxel_coordinates: [], size_voxel: float, triangle: []):
    """
    Проверка на включение проекции меша на плоскость в проекцию вокселя на плоскость
    :param voxel_coordinates: Координаты верхней левой вершины квадрата
    :param size_voxel: размер граней квадрата
    :param triangle: координаты вершин меша
    :return: Параметр bool, означающий закрашивание вокселя
    """
    for vert in triangle:
        res = True
        if not (voxel_coordinates[0] <= vert[0] <= voxel_coordinates[0] + size_voxel
                and voxel_coordinates[1] <= vert[1] <= voxel_coordinates[1] + size_voxel):
            res = False
        if not (voxel_coordinates[0] <= vert[0] <= voxel_coordinates[0] + size_voxel
                and voxel_coordinates[2] <= vert[2] <= voxel_coordinates[2] + size_voxel):
            res = False
        if not (voxel_coordinates[1] <= vert[1] <= voxel_coordinates[1] + size_voxel
                and voxel_coordinates[2] <= vert[2] <= voxel_coordinates[2] + size_voxel):
            res = False
        if res:
            return res
    return False


size = 1
count_mesh = 4
model = return_sample_cube()
size_mod = find_size_model(model)
voxels = get_voxel_model(model, size_mod)
print(voxels)



def test_output(voxels: []):
    test = voxels[len(voxels) - 1]
    for y in test:
        for x in y:
            if x:
                print("#", end="")
            else:
                print(" ", end="")
        print()

test_output(voxels)
