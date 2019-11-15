from OcTree.NodeOcTree import Node


def get_octree(meshes: [], extreme_points: [], size_voxel):
    """
    Строит октдерево
    :param meshes: список мешей
    :param extreme_points: крайние точки модели в формате [[min_x, max_x], [min_y, max_y], [min_z, max_z]]
    :param size_voxel:
    :return:
    """
    max_size_model = max(*[i[1] - i[0] for i in extreme_points])
    first = Node(None, max_size_model, [extreme_points[0][0], extreme_points[1][0], extreme_points[2][0]], meshes)
    first.add_children()
    _fill_tree(first, size_voxel)
    return first


def _fill_tree(node: Node, size_voxel):
    if node.Size <= size_voxel or len(node.Meshes) <= 1:
        return
    _distribution(node)
    for child in node.Children:
        child.add_children()
        _fill_tree(child, size_voxel)


def _distribution(node: Node):
    """
    Распределяет меши в вершине по детям. Оставшиеся сохраняет обратно в Meshes
    :param node: вершина дерева
    :return:
    """
    meshes_on_bounding_boxes = []
    for mesh in node.Meshes:
        bounding_boxes_for_mesh = _get_bounding_box_for_mesh(mesh, node)
        reference = bounding_boxes_for_mesh[0]
        for i in bounding_boxes_for_mesh:
            if 0 in i or i != reference:
                meshes_on_bounding_boxes.append(mesh)
                break
        node.find_child_and_add_mesh(reference, mesh)

    node.Meshes = meshes_on_bounding_boxes


def _get_bounding_box_for_mesh(mesh: [], node: Node):  # Протестированно
    """
    Принимает вершинины меша!!! (без вектора нормали)
    :param mesh:
    :param node:
    :return:
    """
    return [[node.checking_location_point_relative_plane(i, vert) for i in range(3)] for vert in mesh]
