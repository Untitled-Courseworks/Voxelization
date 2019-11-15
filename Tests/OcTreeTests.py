import unittest
from OcTree.NodeOcTree import Node
from Tests.Samples import get_empty_node_with_empty_children
import OcTree.CreateOcTree as Cot


class TestsForFindChildAndAddMesh(unittest.TestCase):

    @staticmethod
    def get_empty_node_with_empty_children(size: float):
        res = Node(None, size, [0, 0, 0], [])
        res.add_children()
        return res

    def test_1(self):
        node = self.get_empty_node_with_empty_children(4)
        node.find_child_and_add_mesh([1, 1, 1], 1)
        self.assertEqual(1, node.Children[0].Meshes[0])

    def test_2(self):
        node = self.get_empty_node_with_empty_children(4)
        node.find_child_and_add_mesh([1, 1, -1], 1)
        self.assertEqual(1, node.Children[1].Meshes[0])

    def test_3(self):
        node = self.get_empty_node_with_empty_children(4)
        node.find_child_and_add_mesh([1, -1, 1], 1)
        self.assertEqual(1, node.Children[2].Meshes[0])

    def test_4(self):
        node = self.get_empty_node_with_empty_children(4)
        node.find_child_and_add_mesh([1, -1, -1], 1)
        self.assertEqual(1, node.Children[3].Meshes[0])

    def test_5(self):
        node = self.get_empty_node_with_empty_children(4)
        node.find_child_and_add_mesh([-1, 1, 1], 1)
        self.assertEqual(1, node.Children[4].Meshes[0])

    def test_6(self):
        node = self.get_empty_node_with_empty_children(4)
        node.find_child_and_add_mesh([-1, -1, 1], 1)
        self.assertEqual(1, node.Children[5].Meshes[0])

    def test_7(self):
        node = self.get_empty_node_with_empty_children(4)
        node.find_child_and_add_mesh([-1, 1, -1], 1)
        self.assertEqual(1, node.Children[6].Meshes[0])

    def test_8(self):
        node = self.get_empty_node_with_empty_children(4)
        node.find_child_and_add_mesh([-1, -1, -1], 1)
        self.assertEqual(1, node.Children[7].Meshes[0])


class TestsGetBoundingBox(unittest.TestCase):

    def test_3_point_mesh(self):
        node = get_empty_node_with_empty_children(4.5)
        mesh = [[0.5, 0.5, 0.5], [1, 1, 1], [1.5, 1.5, 1.5]]
        res = Cot._get_bounding_box_for_mesh(mesh, node)
        self.assertEqual([[-1, -1, -1] for i in range(3)], res)

    def test_3_point_with_extreme_point(self):
        node = get_empty_node_with_empty_children(4)
        mesh = [[0, 0, 0], [1, 1, 1], [1.5, 1.5, 1.5]]
        res = Cot._get_bounding_box_for_mesh(mesh, node)
        self.assertEqual([[-1, -1, -1] for i in range(3)], res)

    def test_3_point_mesh_one_on_bounding_boxes(self):
        node = get_empty_node_with_empty_children(4)
        mesh = [[0.5, 0.5, 0.5], [1, 1, 1], [2, 2, 2]]
        res = Cot._get_bounding_box_for_mesh(mesh, node)
        self.assertEqual([[-1, -1, -1], [-1, -1, -1], [0, 0, 0]], res)

    def test_4_points_mesh(self):
        node = get_empty_node_with_empty_children(4)
        mesh = [[0.5, 0.5, 0.5], [0.7, 0.7, 0.7], [1, 1, 1], [1.5, 1.5, 1.5]]
        res = Cot._get_bounding_box_for_mesh(mesh, node)
        self.assertEqual([[-1, -1, -1] for i in range(4)], res)

    def test_4_points_mesh_on_boundeng_boxes(self):
        node = get_empty_node_with_empty_children(4)
        mesh = [[0, 0, 0], [2, 0, 0], [2, 2, 2], [0, 2, 2]]
        res = Cot._get_bounding_box_for_mesh(mesh, node)
        self.assertEqual([[-1, -1, -1], [0, -1, -1], [0, 0, 0], [-1, 0, 0]], res)


class TestsGetAllVoxelsVertex(unittest.TestCase):

    def test_simple(self):
        node = get_empty_node_with_empty_children()
        res = [i for i in node._get_all_voxels_vertex([0, 0, 0], 1)]
        answ = [[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 1, 1], [1, 0, 0], [1, 0, 1], [1, 1, 0], [1, 1, 1]]
        self.assertEqual(res, answ)

    def test_voxel_on_negative_side(self):
        node = get_empty_node_with_empty_children()
        res = [i for i in node._get_all_voxels_vertex([-4, -4, -4], 2)]
        answ = [[-4, -4, -4], [-4, -4, -2], [-4, -2, -4], [-4, -2, -2], [-2, -4, -4], [-2, -4, -2], [-2, -2, -4],
                [-2, -2, -2]]
        self.assertEqual(res, answ)

    def test_voxel_on_positive_side(self):
        node = get_empty_node_with_empty_children()
        res = [i for i in node._get_all_voxels_vertex([1, 1, 1], 1)]
        answ = [[1, 1, 1], [1, 1, 2], [1, 2, 1], [1, 2, 2], [2, 1, 1], [2, 1, 2], [2, 2, 1], [2, 2, 2]]
        self.assertEqual(res, answ)


class TestsCheckCrossingWithMeshes(unittest.TestCase):

    def test_simple_true(self):
        node = get_empty_node_with_empty_children()
        node.Meshes = [[[1, 1, 1], [2, 3, 2], [3, 3, 3], []]]
        self.assertTrue(node._check_crossing_with_meshes([0, 0, 0], 1))

    def test_with_two_meshes_true(self):
        node = get_empty_node_with_empty_children()
        node.Meshes = [[[1, 1, 1], [2, 3, 2], [3, 3, 3], []], [[2, 2, 2], [3, 4, 3], [4, 4, 4], []]]
        self.assertTrue(node._check_crossing_with_meshes([1, 1, 1], 1))

    def test_with_two_meshes_without_normal_vector_true(self):
        node = get_empty_node_with_empty_children()
        node.Meshes = [[[1, 1, 1], [2, 3, 2], [3, 3, 3]], [[2, 2, 2], [3, 4, 3], [4, 4, 4]]]
        self.assertTrue(node._check_crossing_with_meshes([1, 1, 1], 1))

    def test_simple_false(self):
        node = get_empty_node_with_empty_children()
        node.Meshes = [[[1, 1, 1], [2, 3, 2], [3, 3, 3], []]]
        self.assertFalse(node._check_crossing_with_meshes([0, 0, 0], 0.5))

    def test_with_two_meshes_false(self):
        node = get_empty_node_with_empty_children()
        node.Meshes = [[[1, 1, 1], [2, 3, 2], [3, 3, 3], []], [[2, 2, 2], [3, 4, 3], [4, 4, 4], []]]
        self.assertFalse(node._check_crossing_with_meshes([0, 0, 0], 0.5))

    def test_with_two_meshes_without_normal_vector_false(self):
        node = get_empty_node_with_empty_children()
        node.Meshes = [[[1, 1, 1], [2, 3, 2], [3, 3, 3]], [[2, 2, 2], [3, 4, 3], [4, 4, 4]]]
        self.assertFalse(node._check_crossing_with_meshes([0, 0, 0], 0.5))


if __name__ == '__main__':
    unittest.main()
