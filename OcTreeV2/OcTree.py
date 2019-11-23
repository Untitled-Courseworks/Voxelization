from OcTreeV2.NodeOcTreeV2 import Node
import Crossing


class Octree:

    def __init__(self, objects: [], size_voxel: [], ep: [], is_voxels=False):
        """

        :param objects: объекты для хранения в дереве
        :param size_voxel: размер вокселя
        :param ep: крайние точки модели
        :param is_voxels: объекты дерева - воксели?
        """
        max_size_model = max(*[i[1] - i[0] for i in ep])
        self.Start = Node(None, max_size_model, [point[0] for point in ep])
        self.Start.add_objects(objects)
        self.Size_voxel = size_voxel
        self.Is_voxels = is_voxels

    def fill_tree(self):
        self._fill_tree(self.Start)

    def _fill_tree(self, node: Node):  # Tested
        """
        Заполнение дерева
        :param node: вершина
        :return:
        """
        if node.Size <= self.Size_voxel or str(type(node.Objects)) == "<class 'generator'>" or len(node.Objects) <= 1:
            return
        if len(node.Children) == 0:
            node.add_children()
        node.distribute(self.Is_voxels, self.Size_voxel)
        for child in node.Children:
            self._fill_tree(child)

    def get_first_crossing(self, object_checked, node: Node):
        """
        Предназначена для возвращения первого персечения с мешем, когда меши в дереве
        :param object_checked: воксель
        :param node: проверяемая вершина, для начала поиска указать стартовую
        :return:
        """
        for ob in node.Objects:
            if Crossing.crossing(ob, object_checked, self.Size_voxel):
                return ob
        if len(node.Children) > 0:
            for child in self._get_children_for_checked(self._get_all_voxels_vertex(object_checked, self.Size_voxel), node):
                temp = self.get_first_crossing(object_checked, child)
                if temp is not None:
                    return temp

    def get_all_crossing(self, object_checked, node: Node):  # Tested
        """
        Предназначена для возвращения вокселей, когда они находятся в дереве
        :param object_checked: Меш
        :param node: проверяемая вершина. Для начала поиска указать стартовую
        :return:
        """
        not_crossing = []
        for ob in node.Objects:
            if Crossing.crossing(object_checked, ob, self.Size_voxel):
                yield ob
            else:
                not_crossing.append(ob)
        node.Objects = not_crossing
        if len(node.Children) > 0:
            for child in self._get_children_for_checked(object_checked, node):
                temp = self.get_all_crossing(object_checked, child)
                for i in temp:
                    yield i

    @staticmethod
    def _get_children_for_checked(vertexes: [], node: Node):  # Tested
        """
        Определяет, каких потомков проверять дальше
        :param vertexes список вершин
        :return: ленивый список потомкав
        """
        children = []
        for vert in vertexes:
            location = node.get_location_point(vert)
            if 0 in location:
                continue
            if location not in children:
                children.append(location)
                yield node.find_and_get_child(location)

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
        for x in range(2):
            for y in range(2):
                for z in range(2):
                    yield [x * size + voxel[0], y * size + voxel[1], z * size + voxel[2]]

    @staticmethod
    def get_all_voxels(start_point: [], size_voxel: float, max_size: float):
        x = 0
        while x < max_size:
            y = 0
            while y < max_size:
                z = 0
                while z < max_size:
                    yield [start_point[0] + x, start_point[1] + y, start_point[2] + z]
                    z += size_voxel
                y += size_voxel
            x += size_voxel
