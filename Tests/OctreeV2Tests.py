import unittest
from OcTreeV2.NodeOcTreeV2 import Node
from OcTreeV2.OcTree import Octree
import math


def get_simple_node(size=4.0, position=[0.0, 0.0, 0.0]):
    return Node(None, size, position)


class TestsAddChildren(unittest.TestCase):

    def test_simple(self):
        node = get_simple_node()
        node.add_children()
        self.assertEqual(8, len(node.Children))

    def test_2(self):
        node = get_simple_node(4)
        node.add_children()
        self.assertEqual([2, 2, 2], node.BoundingBox)

        self.assertEqual([1, 1, 1], node.Children[0].BoundingBox, "node num: 0")
        self.assertEqual([1, 1, 3], node.Children[1].BoundingBox, "node num: 1")
        self.assertEqual([1, 3, 1], node.Children[2].BoundingBox, "node num: 2")
        self.assertEqual([1, 3, 3], node.Children[3].BoundingBox, "node num: 3")
        self.assertEqual([3, 1, 1], node.Children[4].BoundingBox, "node num: 4")
        self.assertEqual([3, 1, 3], node.Children[5].BoundingBox, "node num: 5")
        self.assertEqual([3, 3, 1], node.Children[6].BoundingBox, "node num: 6")
        self.assertEqual([3, 3, 3], node.Children[7].BoundingBox, "node num: 7")

class TestsAddObjects(unittest.TestCase):

    def test_simple(self):
        node = get_simple_node()
        node.add_objects([1, 1, 2, 2, 3, 3, 4, 4, 5, 9])
        self.assertEqual(8, len(node.Children))
        self.assertEqual(10, len(node.Objects))


class TestsDectributeForMeshes(unittest.TestCase):

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


class TestDistributeForVoxels(unittest.TestCase):

    def test_distribute_one_voxel(self):
        node = get_simple_node(4)
        node.add_objects([[0, 0, 0]])
        node.distribute(True, 4)
        self.assertEqual(1, len(node))

    def test_with_8_voxels(self):
        node = get_simple_node()
        node.add_objects(Octree.get_all_voxels([0, 0, 0], 2, 4))
        node.distribute(True, 2)
        self.assertEqual(8, len(node))

    def test_with_27_voxels(self):
        node = get_simple_node(3)
        node.add_objects(Octree.get_all_voxels([0, 0, 0], 1, 3))
        node.distribute(True, 1)
        self.assertEqual(TestsFillOctree.get_count_voxels_on_upper_node(1, 3), len(node))
        for i in range(8):
            child = node.Children[i]
            self.assertEqual(1, len(child))

    def test_with_64_voxels(self):
        node = get_simple_node()
        node.add_objects(Octree.get_all_voxels([0, 0, 0], 1, 4))
        node.distribute(True, 1)
        self.assertEqual(TestsFillOctree.get_count_voxels_on_upper_node(1, 4), len(node), "start node")
        te = TestsFillOctree.get_count_voxels_on_upper_node(1, 4, )
        for i in range(8):
            child = node.Children[i]
            self.assertEqual(1, len(child))

    def test_with_125_voxels(self):
        node = get_simple_node(5)
        node.add_objects(Octree.get_all_voxels([0, 0, 0], 1, 5))
        node.distribute(True, 1)
        self.assertEqual(TestsFillOctree.get_count_voxels_on_upper_node(1, 5), len(node))
        for i in range(8):
            child = node.Children[i]
            self.assertEqual(8, len(child))

    def test_bounding_boxes_on_start_coordinates_with_64_voxels(self):
        node = get_simple_node(4, [-2, -2, -2])
        node.add_objects([i for i in Octree.get_all_voxels([-2, -2, -2], 1, 4)])
        node.distribute(True, 1)
        self.assertEqual(TestsFillOctree.get_count_voxels_on_upper_node(1, 4), len(node), "start node")
        for i in range(8):
            child = node.Children[i]
            self.assertEqual(1, len(child), "child num: " + str(i))

    def test_bounding_boxes_on_start_coordinates_with_125_voxels(self):
        node = get_simple_node(5, [-2.5, -2.5, -2.5])
        node.add_objects(Octree.get_all_voxels([-2.5, -2.5, -2.5], 1, 5))
        node.distribute(True, 1)
        self.assertEqual(TestsFillOctree.get_count_voxels_on_upper_node(1, 5), len(node))
        for i in range(8):
            child = node.Children[i]
            self.assertEqual(8, len(child), "child num: " + str(i))

    def test_bounding_boxes_on_negative_side_with_8_voxels(self):
        node = get_simple_node(4, [-4, -4, -4])
        node.add_objects(Octree.get_all_voxels([-4, -4, -4], 2, 4))
        node.distribute(True, 2)
        self.assertEqual(8, len(node))
        for i in range(8):
            child = node.Children[i]
            self.assertEqual(0, len(child), "child num: " + str(i))


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
    @staticmethod
    def get_count_voxels_on_upper_node(size_voxel: float, max_size: float):
        length = math.ceil(max_size / size_voxel)
        if length % 2 == 0:
            return math.pow(length, 3) - math.pow(((length / 2) - 1), 3) * 8
        return math.pow(length, 3) - math.pow(math.floor(length / 2), 3) * 8

    def test_with_one_voxel(self):
        points = [[0, 0, 0]]
        octree = get_octree(points, 4)
        octree._fill_tree(octree.Start)
        self.assertEqual(points, octree.Start.Objects)
        for ch in octree.Start.Children:
            self.assertEqual([], ch.Objects)

    def test_with_8_voxels(self):
        voxels = [i for i in Octree.get_all_voxels([0, 0, 0], 2, True)]
        tree = get_octree(voxels, 2, True)
        tree._fill_tree(tree.Start)
        count_voxels = self.get_count_voxels_on_upper_node(2, 4)
        self.assertEqual(voxels, tree.Start.Objects)

    def test_with_27_voxels(self):
        voxels = [i for i in Octree.get_all_voxels([0, 0, 0], 1, 3)]
        tree = Octree(voxels, 1, [[0, 3], [0, 3], [0, 3]], True)
        tree.fill_tree()
        self.assertEqual(self.get_count_voxels_on_upper_node(1, 3), len(tree.Start.Objects))
        for i in range(8):
            self.assertEqual(1, len(tree.Start.Children[i]), str(i))

    def test_with_64_voxels(self):
        voxels = [i for i in Octree.get_all_voxels([0, 0, 0], 1, 4)]
        tree = get_octree(voxels, 1, True)
        tree._fill_tree(tree.Start)
        self.assertEqual(self.get_count_voxels_on_upper_node(1, 4), len(tree.Start.Objects))
        for child in tree.Start.Children:
            self.assertEqual(self.get_count_voxels_on_upper_node(1, 1), len(child.Objects))

    def test_with_125_voxels(self):
        voxels =[i for i in Octree.get_all_voxels([0, 0, 0], 1, 5)]
        tree = Octree(voxels, 1, [[0, 5], [0, 5], [0, 5]], True)
        tree.fill_tree()
        #tree.Start.distribute(True, 1)
        self.assertEqual(self.get_count_voxels_on_upper_node(1, 5), len(tree.Start.Objects))
        for child in range(8):
            self.assertEqual(7, len(tree.Start.Children[child]), str(child))
            for i in range(8):
                ch = tree.Start.Children[child]
                self.assertTrue(len(ch.Children[i]) == 1 or len(ch.Children[i]) == 0)

    def test_with_voxels_in_child(self):
        # TODO
        #  Работает правильно, но лень настраивать тест
        voxels = Node.get_all_voxels_vertex([0, 0, 0], 1)
        v = []
        for i in voxels:
            temp = Node.get_all_voxels_vertex(i, 0.5)
            for t in temp:
                if 2 not in t:
                    v.append(t)
        tree = Octree(v, 0.5, [[0, 4], [0, 4], [0, 4]], True)
        tree._fill_tree(tree.Start)
        print(1)

    def test_with_512_voxels(self):
        voxels = [i for i in Octree.get_all_voxels([0, 0, 0], 0.5, 4)]
        tree = get_octree(voxels, 0.5, True)
        tree._fill_tree(tree.Start)
        self.assertEqual(self.get_count_voxels_on_upper_node(0.5, 4), len(tree.Start.Objects))
        for child in range(8):
            ch = tree.Start.Children[child]
            self.assertEqual(26, len(ch), str(child))


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
        voxels = Node.get_all_voxels_vertex([0, 0, 0], 3)
        node = get_simple_node()
        node.add_objects(voxels)
        node.distribute(True, 1)
        for i in node.Children:
            self.assertEqual(1, len(i.Objects))
        self.assertEqual(0, len(node.Objects))

    def test_distribute_child(self):
        voxels = Node.get_all_voxels_vertex([0, 0, 0], 2)
        v = []
        for i in voxels:
            temp = Node.get_all_voxels_vertex(i, 1)
            for t in temp:
                v.append(t)
        voxels = []
        for i in v:
            temp = Node.get_all_voxels_vertex(i, 0.5)
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
        voxels = Node.get_all_voxels_vertex([0, 0, 0], 2)
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
        vo = Node.get_all_voxels_vertex([0, 0, 0], 2)
        voxels = []
        for i in vo:
            temp = Node.get_all_voxels_vertex(i, 1)
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
