from OcTreeV2.NodeOcTreeV2 import Node


def get_octree(objects: [], size_voxel: [], ep: [], is_voxel: bool):
    max_size_model = max(*[i[1] - i[0] for i in ep])
    start = Node(None, max_size_model, [point[0] for point in ep], is_voxel)
    start.add_objects(objects)
    _fill_tree(start, size_voxel)
    return start


def _fill_tree(node: Node, size_voxel):
    """
    Заполнение дерева
    :param node: вершина
    :param size_voxel: размер вокселя (как минимальный размер вершины)
    :return:
    """
    if node.Size <= size_voxel or len(node.Objects) <= 1:
        return
    node.redistribution()
    for child in node.Children:
        _fill_tree(child, size_voxel)
