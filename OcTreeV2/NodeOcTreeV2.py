class Node:

    def __init__(self, parent, size_node, coordinate_node: []):
        """
        :param parent: предок вершины
        :param size_node: размер вершины
        :param coordinate_node: координаты вершины
        """
        self.Parent = parent
        self.Size_node = size_node
        self.Coordinate_node = coordinate_node
        div_size = self.Size_node / 2
        self.SeparatingPlanes = [self.Coordinate_node[2] + div_size, self.Coordinate_node[1] + div_size,
                                 self.Coordinate_node[0] + div_size]
        self.Voxels = []
        self.Children = []

    def add_objects(self, objects: []):
        """
        Добавление объектов в вершину и создание потомков
        :param objects: список объектов
        :return:
        """
        self.add_children()
        self.Voxels = objects

    def get_location_point(self, point: []):  # Tested
        """
        Сравнивает положение точки и плоскости
        :param point: проверяемая точка с координатами [x, y, z]
        :return: -1, если координата точки меньше по модулю, чем координыты плоскости, 0 - если лежит на плоскости
        и 1 - если больше по модулю, [yOz, xOz, xOy]
        """
        res = []
        for area in range(3):
            if abs(self.SeparatingPlanes[area] > abs(point[area])):
                res.append(-1)
            elif abs(self.SeparatingPlanes[area] < abs(point[area])):
                res.append(1)
        return res

    def add_children(self):  # Tested
        """
        Добавить потомков в вершину
        :return:
        """

        def get_coordinate(mask: [], div_size):
            mask = [m * div_size for m in mask]
            return [self.Coordinate_node[i] + mask[i] for i in range(3)]

        div_size = self.Size_node / 2
        self.Children = [Node(self, div_size, get_coordinate([x, y, z], div_size))
                         for x in range(2) for y in range(2) for z in range(2)]

    def find_and_get_child(self, pos_point: []):  # Tested
        """
        Ищет по позиционным координатам потомка
        :param pos_point: позиционная координата
        :return:
        """
        # TODO Сделать из этой херни конфетку
        if 0 in pos_point:
            raise Exception("pos_point shouldn't contains 0")

        if pos_point[0] == 1:
            if pos_point[1] == 1:
                if pos_point[2] == 1:
                    return self.Children[7]
                else:
                    return self.Children[6]
            else:
                if pos_point[2] == 1:
                    return self.Children[5]
                else:
                    return self.Children[4]
        else:
            if pos_point[1] == 1:
                if pos_point[2] == 1:
                    return self.Children[3]
                else:
                    return self.Children[2]
            else:
                if pos_point[2] == 1:
                    return self.Children[1]
                else:
                    return self.Children[0]

    def distribute(self, size_voxels=0):
        """
        Разбивает объекты в вершине между детьми
        :return:
        """
        # TODO Протестировать

        for voxel in self.Voxels:
            added_locations = []
            voxel_vertex = self._get_all_voxels_vertex(voxel, size_voxels)
            location_first_vertex = self.get_location_point(voxel_vertex[0])
            self.find_and_get_child(location_first_vertex).Voxels.append(voxel)
            added_locations.append(location_first_vertex)

            for i in voxel_vertex:
                location_vertex = self.get_location_point(i)
                if location_vertex != location_first_vertex and location_vertex not in added_locations:
                    self.find_and_get_child(location_vertex).Voxels.append(voxel)
                    added_locations.append(location_vertex)

        self.Voxels = []

    @staticmethod
    def _get_all_voxels_vertex(voxel: [], size: float):  # Tested
        """
        Генерирует все вершины вокселя
        :param voxel: воксель
        :param size: размер
        :return: ленивый список вершин вокселя
        """
        if size < 0:
            raise Exception("size_voxel can't be less than zero")
        res = []
        for x in range(2):
            for y in range(2):
                for z in range(2):
                    res.append([x * size + voxel[0], y * size + voxel[1], z * size + voxel[2]])
        return res
