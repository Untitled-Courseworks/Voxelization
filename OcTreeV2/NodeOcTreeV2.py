class Node:

    def __init__(self, parent, size, coordinate: [], track_usage: bool):
        """
        :param parent: предок вершины
        :param size: размер вершины
        :param coordinate: координаты вершины
        :param track_usage: True - в списке objects должны содержаться, помимо координат, bool параметр в значении false.
                            False - список objects содержит только координаты
        """
        self.Parent = parent
        self.Size = size
        self.Coordinate = coordinate
        div_size = self.Size / 2
        self.BoundingBox = [self.Coordinate[2] + div_size, self.Coordinate[1] + div_size, self.Coordinate[0] + div_size]
        self.Objects = []
        self.Track_usage = track_usage
        self.Children = []

    def add_objects(self, objects: []):
        """
        Добавление объектов в вершину и распределение по потомкам и самой вершине
        :param objects: список объектов
        :return:
        """
        self._add_children()
        self.Objects = self._distribute(objects)

    def redistribution(self):
        """
        Перераспределение объектов в вершине
        :return:
        """
        self._add_children()
        self.Objects = self._distribute(self.Objects)

    def get_location_point(self, point: []):
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

    def get_crossing_children(self, checked_object: []):
        res = []
        for vert in checked_object:
            location = self.get_location_point(vert)
            res.append(self._find_and_get_child(location))
        return res

    def fill_tree(self, size_voxel):
        """
        Заполнение дерева
        :param node: вершина
        :param size_voxel: размер вокселя (как минимальный размер вершины)
        :return:
        """
        if self.Size <= size_voxel or len(self.Objects) <= 1:
            return
        self.redistribution()
        for child in self.Children:
            child.fill_tree(child, size_voxel)

    def _distribute(self, objects: []):
        on_bounding = []
        for ob in objects:
            location = self.get_location_point(ob[0])
            if 0 in location:
                on_bounding.append(ob)
                continue
            is_added = False
            for v in ob:
                temp = self.get_location_point(v)
                if 0 in temp or temp != location:
                    on_bounding.append(ob)
                    is_added = True
                    break
            if not is_added:
                child = self._find_and_get_child(location)
                child.Objects.append(ob)
        return on_bounding

    def _add_children(self):
        def get_coordinate(mask: [], div_size):
            mask = [m * div_size for m in mask]
            return [self.Coordinate[i] + mask[i] for i in range(3)]

        div_size = self.Size / 2
        self.Children = [Node(self, div_size, get_coordinate([x, y, z], div_size), self.Track_usage)
                         for x in range(2) for y in range(2) for z in range(2)]

    def _find_and_get_child(self, pos_point: []):  # Tested
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

    @staticmethod
    def get_all_voxels_vertex(voxel: [], size: float):  # Tested
        """
        Генерирует все вершины вокселя
        :param voxel: воксель
        :param size: размер
        :return: ленивый список вершин вокселя
        """
        if size < 0:
            raise Exception("size can't be less than zero")
        for x in range(2):
            for y in range(2):
                for z in range(2):
                    yield [x * size + voxel[0], y * size + voxel[1], z * size + voxel[2]]
