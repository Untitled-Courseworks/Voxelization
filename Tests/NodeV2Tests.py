import unittest
from OcTreeV2.NodeOcTreeV2 import Node
from OcTreeV2.OcTree import Octree


def get_simple_node(size = 4):
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


def get_octree(points=[], size=1.0, is_voxel=False):
    return Octree(points, size, [[0, 4], [0, 4], [0, 4]], is_voxel)


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
        octree.fill_tree(octree.Start)
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
        tree.fill_tree(tree.Start)
        self.assertEqual(voxels, tree.Start.Objects)

    def test_with_64_voxels(self):
        voxels = Node._get_all_voxels_vertex([0, 0, 0], 2)
        v = []
        for i in voxels:
            temp = Node._get_all_voxels_vertex(i, 1)
            for t in temp:
                v.append(t)
        tree = get_octree(v, 1, True)
        tree.fill_tree(tree.Start)
        self.assertEqual(56, len(tree.Start.Objects))
        for child in tree.Start.Children:
            self.assertEqual(1, len(child.Objects))

    def test_with_512_voxels(self):
        # TODO fixme
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
        tree.fill_tree(tree.Start)
        #for ch in tree.Start.Children:
            #self.assertEqual(26, len(ch.Objects))





if __name__ == '__main':
    unittest.main()
