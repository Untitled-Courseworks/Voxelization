from OcTree.NodeOcTree import Node


def check_crossing(node: Node, voxel: [], size: float):
    """
    Поиск пересечений
    :param node: Вершина, с которой надо начать поиск
    :param voxel: проверяемый воксель
    :param size: размер вокселя
    :return: True, если есть пересечение и False, если нет
    """
    if node._check_crossing_with_meshes(voxel, size):
        return True

    for n in node._return_crossing_with_voxel_bounding_boxes(voxel, size):
        check_crossing(n, voxel, size)

    return False
