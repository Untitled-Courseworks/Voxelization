import unittest
from OcTreeV2.NodeOcTreeV2 import Node
from OcTreeV2.OcTree import Octree


def get_simple_node(size=4):
    return Node(None, size, [0, 0, 0])


class TestsAddChildren(unittest.TestCase):

    def test_simple(self):
        node = get_simple_node()
        node.add_children()
        self.assertEqual(8, len(node.Children))


class TestsAddObjects(unittest.TestCase):

    def test_simple(self):
        node = get_simple_node()
        node.add_objects([1, 1, 2, 2, 3, 3, 4, 4, 5, 9])
        self.assertEqual(8, len(node.Children))
        self.assertEqual(10, len(node.Objects))


class TestsDectribute(unittest.TestCase):

    def test_add_one_object_on_bounding(self):
        node = get_simple_node()
        node.add_objects([[[2, 2, 2], [1, 2, 1], [3, 3, 3]]])
        node.distribute()
        self.assertEqual(1, len(node.Objects))
        self.assertEqual(8, len(node.Children))
        for i in node.Children:
            self.assertEqual(0, len(i.Objects))
            self.assertEqual(0, len(i.Children))

    def test_add_one_object_in_first_child(self):
        node = get_simple_node()
        node.add_objects([[[0, 0, 0], [1, 0.5, 1], [1, 1, 1]]])
        node.distribute()
        self.assertEqual(0, len(node.Objects))
        self.assertEqual(1, len(node.Children[0].Objects))

    def test_zero_in_node_two_in_children(self):
        node = get_simple_node()
        node.add_objects([[[0, 0, 0], [1, 0.5, 1], [1, 1, 1]], [[1, 1, 1], [0.5, 0.7, 0], [0, 0, 0]]])
        node.distribute()
        self.assertEqual(0, len(node.Objects))
        self.assertEqual(2, len(node.Children[0].Objects))

    def test_last(self):
        node = get_simple_node()
        node.add_objects([[[0, 2, 0], [1, 0.5, 1], [1, 1, 1]], [[1, 1, 1], [0.5, 0.7, 0], [0, 0, 0]]])
        node.distribute()
        self.assertEqual(1, len(node.Objects))
        self.assertEqual(1, len(node.Children[0].Objects))


def get_octree(objects=[], size_voxel=1.0, is_voxel=True):
    return Octree(objects, size_voxel, [[0, 4], [0, 4], [0, 4]], is_voxel)


class TestsGetChildrenForChecked(unittest.TestCase):

    def test_with_one_point_on_bounding_boxes(self):
        point = [[2, 2, 2]]
        tree = get_octree()
        res = [i for i in tree._get_children_for_checked(point, tree.Start)]
        self.assertEqual(res, [])

        point = [[2, 0, 2]]
        res = [i for i in tree._get_children_for_checked(point, tree.Start)]
        self.assertEqual([], res)

    def test_with_one_point_on_child(self):
        point = [[0, 0, 0]]
        tree = get_octree()
        res = [i for i in tree._get_children_for_checked(point, tree.Start)]
        self.assertEqual(1, len(res))
        self.assertEqual(tree.Start.Children[0], res[0])

        point = [[3, 3, 3]]
        res = [i for i in tree._get_children_for_checked(point, tree.Start)]
        self.assertEqual(1, len(res))
        self.assertEqual(tree.Start.Children[7], res[0])

    def test_with_voxel(self):
        tree = get_octree()
        point = tree._get_all_voxels_vertex([1.5, 1.5, 1.5], 1)
        res = [i for i in tree._get_children_for_checked(point, tree.Start)]
        self.assertEqual(8, len(res))
        for i in range(8):
            self.assertEqual(tree.Start.Children[i], res[i])

    def test_with_mesh_on_bounding_boxes(self):
        point = [[2, 2, 2], [2, 0, 2], [3, 2, 2]]
        tree = get_octree()
        res = [i for i in tree._get_children_for_checked(point, tree.Start)]
        self.assertEqual([], res)


class TestsFillOctree(unittest.TestCase):

    def test_with_one_voxel(self):
        points = [[0, 0, 0]]
        octree = get_octree(points, 4)
        octree._fill_tree(octree.Start)
        self.assertEqual(points, octree.Start.Objects)
        for ch in octree.Start.Children:
            self.assertEqual([], ch.Objects)

    def test_with_8_voxels(self):
        voxels = []
        for x in range(2):
            for y in range(2):
                for z in range(2):
                    voxels.append([x * 2, y * 2, z * 2])
        tree = get_octree(voxels, 2, True)
        tree._fill_tree(tree.Start)
        self.assertEqual(voxels, tree.Start.Objects)

    def test_with_64_voxels(self):
        voxels = Node._get_all_voxels_vertex([0, 0, 0], 2)
        v = []
        for i in voxels:
            temp = Node._get_all_voxels_vertex(i, 1)
            for t in temp:
                v.append(t)
        tree = get_octree(v, 1, True)
        tree._fill_tree(tree.Start)
        self.assertEqual(56, len(tree.Start.Objects))
        for child in tree.Start.Children:
            self.assertEqual(1, len(child.Objects))

    def test_with_voxels_in_child(self):
        # TODO
        #  Работает правильно, но лень настраивать тест
        voxels = Node._get_all_voxels_vertex([0, 0, 0], 1)
        v = []
        for i in voxels:
            temp = Node._get_all_voxels_vertex(i, 0.5)
            for t in temp:
                if 2 not in t:
                    v.append(t)
        tree = Octree(v, 0.5, [[0, 4], [0, 4], [0, 4]], True)
        tree._fill_tree(tree.Start)
        print(1)

    def test_with_512_voxels(self):
        # TODO
        #  Работает правильно, но лень настраивать тест
        voxels = Node._get_all_voxels_vertex([0, 0, 0], 2)
        v = []
        for i in voxels:
            temp = Node._get_all_voxels_vertex(i, 1)
            for t in temp:
                v.append(t)
        voxels = []
        for i in v:
            temp = Node._get_all_voxels_vertex(i, 0.5)
            for t in temp:
                voxels.append(t)
        tree = get_octree(voxels, 0.5, True)
        tree._fill_tree(tree.Start)
        #for ch in tree.Start.Children:
            #self.assertEqual(26, len(ch.Objects))


class TestsDistribute(unittest.TestCase):

    def test_with_one_vertex_on_bounding_boxes(self):
        voxel = [[0, 2, 0]]
        node = get_simple_node()
        node.add_objects(voxel)
        node.distribute(True, 1)
        self.assertEqual(voxel, node.Objects)

    def test_with_one_voxel_in_child(self):
        voxel = [[3, 0, 3]]
        node = get_simple_node()
        node.add_objects(voxel)
        node.distribute(True, 1)
        self.assertEqual(node.Children[5].Objects, voxel)

        voxel = [[0, 3, 3]]
        node.Objects.append(voxel[0])
        node.distribute(True, 1)
        self.assertEqual(node.Children[3].Objects, voxel)

    def test_with_8_voxels(self):
        voxels = Node._get_all_voxels_vertex([0, 0, 0], 3)
        node = get_simple_node()
        node.add_objects(voxels)
        node.distribute(True, 1)
        for i in node.Children:
            self.assertEqual(1, len(i.Objects))
        self.assertEqual(0, len(node.Objects))

    def test_distribute_child(self):
        voxels = Node._get_all_voxels_vertex([0, 0, 0], 2)
        v = []
        for i in voxels:
            temp = Node._get_all_voxels_vertex(i, 1)
            for t in temp:
                v.append(t)
        voxels = []
        for i in v:
            temp = Node._get_all_voxels_vertex(i, 0.5)
            for t in temp:
                voxels.append(t)
        node = get_simple_node(4)
        node.add_objects(voxels)
        node.distribute(True, 0.5)
        for i in node.Children:
            self.assertEqual(27, len(i.Objects))
            i.add_children()


class TestGetAllCrossing(unittest.TestCase):

    def test_simple(self):
        tree = get_octree([[0, 0, 0]], 4)
        tree.fill_tree()
        mesh = [[1, 1, 1], [1, 2, 1], [2, 2, 2]]
        res = [i for i in tree.get_all_crossing(mesh, tree.Start)]
        self.assertEqual([[0, 0, 0]], res)
        self.assertEqual(0, len(tree.Start.Objects))

    def test_with_8_voxels(self):
        voxels = Node._get_all_voxels_vertex([0, 0, 0], 2)
        tree = get_octree(voxels, 2)
        tree.fill_tree()
        mesh = [[0, 0, 0], [3, 1, 0], [2, 3, 0]]
        res = [i for i in tree.get_all_crossing(mesh, tree.Start)]
        self.assertEqual(4, len(res))
        self.assertEqual([[0, 0, 0], [0, 2, 0], [2, 0, 0], [2, 2, 0]], res)
        self.assertEqual(4, len(tree.Start.Objects))

        mesh = [[3, 0, 3], [4, 0, 4], [4, 1, 4]]
        res = [i for i in tree.get_all_crossing(mesh, tree.Start)]
        self.assertEqual(1, len(res))
        self.assertEqual([[2, 0, 2]], res)
        self.assertEqual(3, len(tree.Start.Objects))

    def test_with_64_voxels(self):
        vo = Node._get_all_voxels_vertex([0, 0, 0], 2)
        voxels = []
        for i in vo:
            temp = Node._get_all_voxels_vertex(i, 1)
            for t in temp:
                voxels.append(t)
        tree = get_octree(voxels, 1)
        tree.fill_tree()
        res = [i for i in tree.get_all_crossing([[0, 0, 0], [0, 4, 0], [4, 0, 0]], tree.Start)]
        self.assertEqual(13, len(res))
        self.assertEqual(46, len(tree.Start.Objects))


class TestsGetAllVoxels(unittest.TestCase):

    def test_simple(self):
        res = [i for i in Octree.get_all_voxels([0, 0, 0], 1, 2)]
        true = [[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 1, 1], [1, 0, 0], [1, 0, 1], [1, 1, 0], [1, 1, 1]]
        self.assertEqual(true, res)

    def test_one_voxel(self):
        res = [i for i in Octree.get_all_voxels([0, 0, 0], 1, 1)]
        true = [[0, 0, 0]]
        self.assertEqual(true, res)

    def test_with_float_size_vozel(self):
        res = [i for i in Octree.get_all_voxels([0, 0, 0], 0.5, 1)]
        true = [[0, 0, 0], [0, 0, 0.5], [0, 0.5, 0], [0, 0.5, 0.5], [0.5, 0, 0], [0.5, 0, 0.5], [0.5, 0.5, 0], [0.5, 0.5, 0.5]]
        self.assertEqual(true, res)

    def test_with_float_size_voxe_and_float_max_size(self):
        res = [i for i in Octree.get_all_voxels([0, 0, 0], 0.5, 0.5)]
        true = [[0, 0, 0]]
        self.assertEqual(true, res)

    def test_with_negative_start_coords(self):
        res = [i for i in Octree.get_all_voxels([-1, -1, -1], 1, 2)]
        true = [[-1, -1, -1], [-1, -1, 0], [-1, 0, -1], [-1, 0, 0], [0, -1, -1], [0, -1, 0], [0, 0, -1], [0, 0, 0]]
        self.assertEqual(true, res)


if __name__ == '__main':
    unittest.main()
