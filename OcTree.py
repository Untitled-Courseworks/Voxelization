class Node:

    def __init__(self, parent, size, coordinate, meshes):
        self.Parent = parent
        self.Size = size
        self.Coordinate = coordinate
        div_size = self.Size / 2
        self.BoundingBox = [self.Coordinate[2] + div_size, self.Coordinate[1] + div_size, self.Coordinate[0] + div_size]
        self.Meshes = meshes
        self.Children = []

    def checking_location_point_relative_plane(self, area: int, point: []):
        """
        Сравнивает положение точки и плоскости
        :param area: плоскость, 0 - xOy, 1 - xOz, 2 - yOz
        :param point: проверяемая точка с координатами [x, y, z]
        :return: -1, если координата точки меньше по модулю, чем координыты плоскости, 0 - если лежит на плоскости
        и 1 - если больше по модулю
        """
        if abs(self.BoundingBox[area] > abs(point[area])):
            return -1
        elif abs(self.BoundingBox[area] < abs(point[area])):
            return 1
        return 0

    def add_children(self):
        def get_coordinate(mask: []):
            return [self.Coordinate[i] + mask[i] for i in range(3)]
        div_size = self.Size / 2
        self.Children.append(Node(self, div_size, get_coordinate([div_size, div_size, div_size]), []))
        self.Children.append(Node(self, div_size, get_coordinate([0, div_size, div_size]), []))
        self.Children.append(Node(self, div_size, get_coordinate([div_size, div_size, 0]), []))
        self.Children.append(Node(self, div_size, get_coordinate([0, div_size, 0]), []))
        self.Children.append(Node(self, div_size, get_coordinate([div_size, 0, div_size]), []))
        self.Children.append(Node(self, div_size, get_coordinate([0, 0, div_size]), []))
        self.Children.append(Node(self, div_size, get_coordinate([div_size, 0, 0]), []))
        self.Children.append(Node(self, div_size, get_coordinate([0, 0, 0]), []))


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
    fill_tree(first, size_voxel)
    return first


def fill_tree(node: Node, size_voxel):
    if node.Size <= size_voxel or len(node.Meshes) <= 1:
        return
    distribution(node)
    for child in node.Children:
        child.add_children()
        fill_tree(child, size_voxel)


# TODO Убрать
def for_tested(node: Node):
    points_on_bounding_boxes = []
    for vert in node.Meshes:
        temp = [node.checking_location_point_relative_plane(i, vert) for i in range(3)]
        if 0 in temp:
            points_on_bounding_boxes.append(vert)
            continue
        find_child_and_add_mesh(temp, vert, node)
    node.Meshes = points_on_bounding_boxes


def distribution(node: Node):
    """
    Распределяет меши в вершине по детям. Оставшиеся сохраняет обратно в Meshes
    :param node: вершина дерева
    :return:
    """
    def get_point_bounding_box(meshes_on_bounding_boxes: [], node: Node, vert: []):
        bounding_box = []
        for i in range(3):
            temp = node.checking_location_point_relative_plane(i, vert)
            if temp == 0:
                meshes_on_bounding_boxes.append(mesh)
                return None
            bounding_box.append(temp)
        return bounding_box

    meshes_on_bounding_boxes = []
    for mesh in node.Meshes:
        bounding_box = get_point_bounding_box(meshes_on_bounding_boxes, node, mesh[0])
        if bounding_box is None:
            continue
        is_added = False
        for vert in range(1, len(mesh) - 1):
            temp = get_point_bounding_box(meshes_on_bounding_boxes, node, mesh[vert])
            if temp is None:
                break
            if temp != bounding_box:
                meshes_on_bounding_boxes.append(mesh)
                is_added = True
                break
        if not is_added:
            find_child_and_add_mesh(bounding_box, mesh, node)
    node.Meshes = meshes_on_bounding_boxes


def find_child_and_add_mesh(pos_point:[], mesh: [], node: Node):  # Протестированно
    # TODO Сделать из этой херни конфетку
    if 0 in pos_point:
        raise Exception("pos_point shouldn't contains 0")

    if pos_point[0] == 1:
        if pos_point[1] == 1:
            if pos_point[2] == 1:
                node.Children[0].Meshes.append(mesh)
            else:
                node.Children[1].Meshes.append(mesh)
        else:
            if pos_point[2] == 1:
                node.Children[2].Meshes.append(mesh)
            else:
                node.Children[3].Meshes.append(mesh)
    else:
        if pos_point[1] == 1:
            if pos_point[2] == 1:
                node.Children[4].Meshes.append(mesh)
            else:
                node.Children[6].Meshes.append(mesh)
        else:
            if pos_point[2] == 1:
                node.Children[5].Meshes.append(mesh)
            else:
                node.Children[7].Meshes.append(mesh)
