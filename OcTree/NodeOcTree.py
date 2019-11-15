import Crossing


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
        # Это вынужденная мера
        self.Children.append(Node(self, div_size, get_coordinate([div_size, div_size, div_size]), []))
        self.Children.append(Node(self, div_size, get_coordinate([0, div_size, div_size]), []))
        self.Children.append(Node(self, div_size, get_coordinate([div_size, div_size, 0]), []))
        self.Children.append(Node(self, div_size, get_coordinate([0, div_size, 0]), []))
        self.Children.append(Node(self, div_size, get_coordinate([div_size, 0, div_size]), []))
        self.Children.append(Node(self, div_size, get_coordinate([0, 0, div_size]), []))
        self.Children.append(Node(self, div_size, get_coordinate([div_size, 0, 0]), []))
        self.Children.append(Node(self, div_size, get_coordinate([0, 0, 0]), []))

    def check_crossing_with_meshes(self, voxel: [], size_voxel: float):
        for mesh in self.Meshes:
            if Crossing.crossing(mesh, voxel, size_voxel):
                return True
        return False

    def return_crossing_with_voxel_bounding_boxes(self, voxel: [], size_voxel: float):
        for vert in self._get_all_voxels_vertex(voxel, size_voxel):
            location = [self.checking_location_point_relative_plane(i, vert) for i in range(3)]
            yield self.find_and_get_child(location)

    def find_and_get_child(self, pos_point: []):  # Протестированно
        # TODO Сделать из этой херни конфетку
        if 0 in pos_point:
            raise Exception("pos_point shouldn't contains 0")

        if pos_point[0] == 1:
            if pos_point[1] == 1:
                if pos_point[2] == 1:
                    return self.Children[0]
                else:
                    return self.Children[1]
            else:
                if pos_point[2] == 1:
                    return self.Children[2]
                else:
                    return self.Children[3]
        else:
            if pos_point[1] == 1:
                if pos_point[2] == 1:
                    return self.Children[4]
                else:
                    return self.Children[6]
            else:
                if pos_point[2] == 1:
                    return self.Children[5]
                else:
                    return self.Children[7]

    def find_child_and_add_mesh(self, pos_point: [], mesh: []):  # Протестированно
        self.find_and_get_child(pos_point).Meshes.append(mesh)

    @staticmethod
    def _get_all_voxels_vertex(voxel: [], size: float):  # Протестированно
        if size < 0:
            raise Exception("size can't be less than zero")
        for x in range(2):
            for y in range(2):
                for z in range(2):
                    yield [x * size + voxel[0], y * size + voxel[1], z * size + voxel[2]]