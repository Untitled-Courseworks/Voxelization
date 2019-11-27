class Node:

    def __init__(self, parent, size, coordinate: []):
        """
        :param parent: предок вершины
        :param size: размер вершины
        :param coordinate: координаты вершины
        """
        self.Parent = parent
        self.Size = size
        self.Coordinate = coordinate
        div_size = self.Size / 2
        self.BoundingBox = [self.Coordinate[2] + div_size, self.Coordinate[1] + div_size, self.Coordinate[0] + div_size]
        self.Objects = []
        self.Children = []

    def add_objects(self, objects: []):
        """
        Добавление объектов в вершину и создание потомков
        :param objects: список объектов
        :return:
        """
        self.add_children()
        self.Objects = objects

    def get_location_point(self, point: []):  # Tested
        """
        Сравнивает положение точки и плоскости
        :param point: проверяемая точка с координатами [x, y, z]
        :return: -1, если координата точки меньше по модулю, чем координыты плоскости, 0 - если лежит на плоскости
        и 1 - если больше по модулю, [yOz, xOz, xOy]
        """
        res = []
        for area in range(3):
            if (self.BoundingBox[area]) > (point[area]):
                res.append(-1)
            elif (self.BoundingBox[area]) < (point[area]):
                res.append(1)
            else:
                res.append(0)
        return res

    def add_children(self):  # Tested
        """
        Добавить потомков в вершину
        :return:
        """

        def get_coordinate(mask: [], div_size):
            mask = [m * div_size for m in mask]
            return [self.Coordinate[i] + mask[i] for i in range(3)]

        div_size = self.Size / 2
        self.Children = [Node(self, div_size, get_coordinate([x, y, z], div_size))
                         for x in range(2) for y in range(2) for z in range(2)]

    def get_child(self, pos_point: []):  # Tested
        """
        :param pos_point: позиционная координата
        :return:
        """
        if 0 in pos_point:
            raise Exception("pos_point shouldn't contains 0")
        return self.Children[self._get_num_children_from_location(pos_point)]

    def _get_num_children_from_location(self, location: []):
        if location == [-1, -1, -1]:
            return 0
        elif location == [-1, -1, 1]:
            return 1
        elif location == [-1, 1, -1]:
            return 2
        elif location == [-1, 1, 1]:
            return 3
        elif location == [1, -1, -1]:
            return 4
        elif location == [1, -1, 1]:
            return 5
        elif location == [1, 1, -1]:
            return 6
        elif location == [1, 1, 1]:
            return 7

    def distribute(self, is_voxels=True, size_voxels=0):
        """
        Разбивает объекты в вершине между вершиной и детьми
        :return:
        """
        node_objects = []
        for objects in self.Objects:
            first_diagonal_vertex = objects
            second_diagonal_vertex = [i + size_voxels for i in objects]
            if self._compare_diagonal_vertexes(first_diagonal_vertex, second_diagonal_vertex):
                node_objects.append(objects)
                continue
            self.get_child(self.get_location_point(first_diagonal_vertex)).Objects.append(objects)
        self.Objects = node_objects

    def _compare_diagonal_vertexes(self, first_vertex, second_vertex) -> bool:
        location_first_vertex = self.get_location_point(first_vertex)
        location_second_vertex = self.get_location_point(second_vertex)
        return location_first_vertex != location_second_vertex or (0 in location_first_vertex in location_second_vertex)

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

    def __len__(self):
        return len(self.Objects)
