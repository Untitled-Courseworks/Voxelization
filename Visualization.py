from vpython import *


def _get_voxel(x, y, z):
    a = 0.1  # Длина вокселя
    b = a / 2  # Половина длины вокселя
    c = 0.02  # Толщина ребра
    d = 0.001  # Толщина грани
    _get_verges(a, b, c, d, x, y, z)
    _get_borders(a, b, c, x, y, z)


def _get_verges(a, b, c, d, x, y, z):
    """
    pos - позиция, задается => vec(x, y, z), где x/y/z - любое число
    size - размер (в нашем случае он не важен, т.к. все воксели одинаковые)
    color - цвет, задается => vec(r, g, b), где r/g/b - [0,1]
    shininess - Блеск (0 - off, 1 - on(по умол.))
    emissive - Игнорирование источников света (True - игнор., False - не игнор.(по умол.))
    """
    m = (b - 0.5 * d)  # Сдвиг грани от центра вокселя
    p = (a - 2 * c)  # Длина грани между ребрами
    box(pos=vec(x, y, z + m), size=vec(p, p, d), color=color.green, shininess=0, emissive=True)  # front(x, y)
    box(pos=vec(x, y, z - m), size=vec(p, p, d), color=color.green, shininess=0, emissive=True)  # back(x, y)
    box(pos=vec(x - m, y, z), size=vec(d, p, p), color=color.green, shininess=0, emissive=True)  # left(y, z)
    box(pos=vec(x + m, y, z), size=vec(d, p, p), color=color.green, shininess=0, emissive=True)  # right(y, z)
    box(pos=vec(x, y + m, z), size=vec(p, d, p), color=color.green, shininess=0, emissive=True)  # up(x, z)
    box(pos=vec(x, y - m, z), size=vec(p, d, p), color=color.green, shininess=0, emissive=True)  # down(x, z)


def _get_borders(a, b, c, x, y, z):
    n = (b - 0.5 * c)  # Сдвиг ребра от центра вокселя
    box(pos=vec(x, y - n, z + n), size=vec(a, c, c), color=color.red, shininess=0, emissive=True)  # перед низ
    box(pos=vec(x, y + n, z + n), size=vec(a, c, c), color=color.red, shininess=0, emissive=True)  # перед верх
    box(pos=vec(x - n, y, z + n), size=vec(c, a, c), color=color.red, shininess=0, emissive=True)  # перед лево
    box(pos=vec(x + n, y, z + n), size=vec(c, a, c), color=color.red, shininess=0, emissive=True)  # перед право
    box(pos=vec(x, y - n, z - n), size=vec(a, c, c), color=color.red, shininess=0, emissive=True)  # зад низ
    box(pos=vec(x, y + n, z - n), size=vec(a, c, c), color=color.red, shininess=0, emissive=True)  # зад верх
    box(pos=vec(x - n, y, z - n), size=vec(c, a, c), color=color.red, shininess=0, emissive=True)  # зад лево
    box(pos=vec(x + n, y, z - n), size=vec(c, a, c), color=color.red, shininess=0, emissive=True)  # зад право
    box(pos=vec(x - n, y - n, z), size=vec(c, c, a), color=color.red, shininess=0, emissive=True)  # лево низ
    box(pos=vec(x - n, y + n, z), size=vec(c, c, a), color=color.red, shininess=0, emissive=True)  # лево верх
    box(pos=vec(x + n, y - n, z), size=vec(c, c, a), color=color.red, shininess=0, emissive=True)  # право низ
    box(pos=vec(x + n, y + n, z), size=vec(c, c, a), color=color.red, shininess=0, emissive=True)  # право верх


def get_model(coords: []):
    """
    Метод, визуализирующий воксели.
    Принимает массив вида : [[x, y, z], [x, y, z], ...], где x/y/z/ - координаты вокселя
    Импортировать и вызывать его
    """
    # TODO временно
    #if len(coords) == 0:
        #raise ValueError("Input array is empty")  # Проверка на пустой массив без данных (если не нужен, можно урать)
    for voxel in coords:
        _get_voxel(voxel[0], voxel[1], voxel[2])
