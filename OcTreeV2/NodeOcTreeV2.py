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
            if abs(self.BoundingBox[area] > abs(point[area])):
                res.append(-1)
            elif abs(self.BoundingBox[area] < abs(point[area])):
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

    def distribute(self, is_voxels=False, size_voxels=0):
        """
        Разбивает объекты в вершине между вершиной и детьми
        :return:
        """
        try:
            node_objects = []
            for ob in self.Objects:
                object_vertex = ob
                if is_voxels:
                    object_vertex = self._get_all_voxels_vertex(ob, size_voxels)
                location = self.get_location_point(object_vertex[0])
                if 0 in location:
                    node_objects.append(ob)
                    continue
                is_added = False
                for i in object_vertex:
                    temp_location = self.get_location_point(i)
                    if 0 in temp_location or temp_location != location:
                        node_objects.append(ob)
                        is_added = True
                        break
                if not is_added:
                    self.find_and_get_child(location).Objects.append(ob)
            self.Objects = node_objects
        except:
            raise Exception("error")

    @staticmethod
    def _get_all_voxels_vertex(voxel: [], size: float):  # Tested
        """
        Генерирует все вершины вокселя
        :param voxel: воксель
        :param size: размер
        :return: ленивый список вершин вокселя
        """
        if size < 0:
            raise Exception("size can't be less than zero")
        res = []
        for x in range(2):
            for y in range(2):
                for z in range(2):
                    res.append([x * size + voxel[0], y * size + voxel[1], z * size + voxel[2]])
        return res
