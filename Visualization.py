from vpython import *


def _get_voxel(x, y, z):
    """
    pos - позиция, задается => vec(x, y, z), где x/y/z - любое число
    size - размер (в нашем случае он не важен, т.к. все воксели одинаковые)
    color - цвет, задается => vec(r, g, b), где r/g/b - [0,1]
    shininess - Блеск (0 - off, 1 - on(по умол.))
    emissive - Игнорирование источников света (True - игнор., False - не игнор.(по умол.))
    """
    box(pos=vec(x, y, z + 0.5), size=vec(1, 1, 0.001), color=color.green, shininess=0, emissive=True)  # front(x, y)
    box(pos=vec(x, y, z - 0.5), size=vec(1, 1, 0.001), color=color.green, shininess=0, emissive=True)  # back(x, y)
    box(pos=vec(x - 0.5, y, z), size=vec(0.001, 1, 1), color=color.green, shininess=0, emissive=True)  # left(y, z)
    box(pos=vec(x + 0.5, y, z), size=vec(0.001, 1, 1), color=color.green, shininess=0, emissive=True)  # right(y, z)
    box(pos=vec(x, y + 0.5, z), size=vec(1, 0.001, 1), color=color.green, shininess=0, emissive=True)  # up(x, z)
    box(pos=vec(x, y - 0.5, z), size=vec(1, 0.001, 1), color=color.green, shininess=0, emissive=True)  # down(x, z)


def get_model(coords: []):
    """
    Метод, визуализирующий воксели.
    Принимает массив вида : [[x, y, z], [x, y, z], ...], где x/y/z/ - координаты вокселя
    Импортировать и вызывать его
    """
    if len(coords) == 0:
        raise ValueError("Input array is empty")  # Проверка на пустой массив без данных (если не нужен, можно урать)
    for voxel in coords:
        _get_voxel(voxel[0], voxel[1], voxel[2])
