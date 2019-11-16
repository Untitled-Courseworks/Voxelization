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

    def test_with_zero_meshes_false(self):
        node = get_empty_node_with_empty_children()
        self.assertFalse(node._check_crossing_with_meshes([0, 0, 0], 1))


class TestsGetCrossingWithVoxelBoundingBoxes(unittest.TestCase):

    def test_simple(self):
        node = get_empty_node_with_empty_children(4)
        res = [i for i in node._get_crossing_with_voxel_bounding_boxes([1, 1, 1], 0.5)]
        self.assertEqual(1, len(res))
        self.assertEqual(res[0], node.Children[7])

    def test_voxel_on_bounding_boxes(self):
        node = get_empty_node_with_empty_children(4)
        res = [i for i in node._get_crossing_with_voxel_bounding_boxes([0, 0, 0], 2)]
        self.assertEqual(1, len(res))
        self.assertEqual(res[0], node.Children[7])

    def test_voxel_on_bounding_boxes_cildren_node(self):
        node = get_empty_node_with_empty_children(4)
        child = node.Children[7]
        child.add_children()
        res = [i for i in child._get_crossing_with_voxel_bounding_boxes([0, 0, 0], 1)]
        self.assertEqual(1, len(res))
        self.assertEqual(res[0], child.Children[7])

    def test_voxel_on_center(self):
        node = get_empty_node_with_empty_children(4)
        res = [i for i in node._get_crossing_with_voxel_bounding_boxes([1, 1, 1], 2)]
        self.assertEqual(8, len(res))
        for child in node.Children:
            self.assertTrue(child in res)

    def test_voxel_is_max(self):
        node = get_empty_node_with_empty_children()
        res = [i for i in node._get_crossing_with_voxel_bounding_boxes([0, 0, 0], 1)]
        self.assertEqual(8, len(res))
        for child in node.Children:
            self.assertTrue(child in res)


class TestsCheckCrossing(unittest.TestCase):

    def get_node_with_meshes_on_first_lvl(self):
        node = get_empty_node_with_empty_children(4)
        node.Meshes = [[[2, 2, 2], [2, 2, 3], [1, 1, 1]], [[0, 0, 0], [1, 1, 1], [1, 2, 1]]]
        return node

    def test_crossing_on_first_lvl_true(self):
        node = self.get_node_with_meshes_on_first_lvl()
        res = node.check_crossing([1, 1, 1], 1)
        self.assertTrue(res)

        res = node.check_crossing([0, 0, 0], 2)
        self.assertTrue(res)

    def test_crossing_on_first_lvl_false(self):
        node = self.get_node_with_meshes_on_first_lvl()
        res = node.check_crossing([3, 3, 3], 1)
        self.assertFalse(res)

        res = node.check_crossing([3, 3, 3], 2)
        self.assertFalse(res)

    def test_crossing_on_first_lvl_max_voxel_true(self):
        node = self.get_node_with_meshes_on_first_lvl()
        res = node.check_crossing([0, 0, 0], 4)
        self.assertTrue(res)

    def test_crossing_on_second_lvl_true(self):
        meshes = [[[0.5, 0.5, 0.5], [1, 0.5, 1], [1, 1, 1]], [[0.6, 0.6, 0.6], [0.6, 0.7, 0.7], [1, 1, 1]]]
        node = Cot.get_octree(meshes, [[0, 4], [0, 4], [0, 4]], 1)
        res = node.check_crossing([1, 1, 1], 1)
        self.assertTrue(res)

    def test_crossing_on_third_lvl_true(self):
        meshes = [[[0.5, 0.5, 0.5], [1, 0.5, 1], [1, 1, 1]], [[0.6, 0.6, 0.6], [0.6, 0.7, 0.7], [0.5, 0.5, 0.5]]]
        node = Cot.get_octree(meshes, [[0, 4], [0, 4], [0, 4]], 1)
        res = node.check_crossing([0.5, 0.5, 0.5], 1)
        self.assertTrue(res)

    def test_crossing_on_third_lvl_false(self):
        meshes = [[[0.5, 0.5, 0.5], [1, 0.5, 1], [1, 1, 1]], [[0.6, 0.6, 0.6], [0.6, 0.7, 0.7], [0.5, 0.5, 0.5]]]
        node = Cot.get_octree(meshes, [[0, 4], [0, 4], [0, 4]], 1)
        res = node.check_crossing([2, 2, 2], 1)
        self.assertFalse(res)


class TestsDistribution(unittest.TestCase):

    def test_add_mesh_on_first_lvl(self):
        node = get_empty_node_with_empty_children(4)
        mesh = [[[0, 0, 0], [2, 2, 2], [2, 3, 3]]]
        node.Meshes = mesh
        Cot._distribution(node)
        self.assertEqual(1, len(node.Meshes))
        self.assertEqual(mesh, node.Meshes)

    def test_add_mesh_on_second_lvl(self):
        node = get_empty_node_with_empty_children(4)
        mesh = [[[3, 3, 3], [3, 3.5, 3], [3.5, 3, 3]]]
        node.Meshes = mesh
        Cot._distribution(node)
        self.assertEqual(0, len(node.Meshes))
        self.assertEqual(1, len(node.Children[0].Meshes))
        self.assertEqual(mesh, node.Children[0].Meshes)


class TestsFillTree(unittest.TestCase):

    def test_add_first_lvl_mesh(self):
        node = get_empty_node_with_empty_children(4)
        mesh = [[[1, 1, 1], [1, 2, 1], [2, 2, 2]]]
        node.Meshes = mesh
        Cot._fill_tree(node, 0.5)
        self.assertEqual(1, len(node.Meshes))
        self.assertEqual(mesh, node.Meshes)

    def test_add_second_lvl_mesh(self):
        node = get_empty_node_with_empty_children(4)
        meshes = [[[0.5, 0.5, 0.5], [1, 0.5, 1], [1, 1, 1]], [[0.6, 0.6, 0.6], [0.6, 0.7, 0.7], [1, 1, 1]]]
        node.Meshes = meshes
        Cot._fill_tree(node, 0.5)
        self.assertEqual(2, len(node.Children[7].Meshes))

    def test_dont_add_man_size(self):
        node = get_empty_node_with_empty_children(4)
        meshes = [[[0.5, 0.5, 0.5], [1, 0.5, 1], [1, 1, 1]], [[0.6, 0.6, 0.6], [0.6, 0.7, 0.7], [0.5, 0.5, 0.5]]]
        node.Meshes = meshes
        Cot._fill_tree(node, 2)
        self.assertEqual(2, len(node.Children[7].Meshes))

    def test_add_third_lvl(self):
        node = get_empty_node_with_empty_children(4)
        meshes = [[[0.5, 0.5, 0.5], [1, 0.5, 1], [1, 1, 1]], [[0.6, 0.6, 0.6], [0.6, 0.7, 0.7], [0.5, 0.5, 0.5]]]
        node.Meshes = meshes
        Cot._fill_tree(node, 1)
        self.assertEqual(1, len(node.Children[7].Children[7].Meshes))
        self.assertEqual(1, len(node.Children[7].Meshes))

    def test_dont_add_one_mesh(self):
        node = get_empty_node_with_empty_children(4)
        meshes = [[[0.6, 0.6, 0.6], [0.6, 0.7, 0.7], [0.5, 0.5, 0.5]]]
        node.Meshes = meshes
        Cot._fill_tree(node, 1)
        self.assertEqual(1, len(node.Meshes))


class TestsGetOctree(unittest.TestCase):

    def test_create_node_with_one_mesh(self):
        meshes = [[[1, 1, 1], [1, 1.5, 1], [1, 1, 1.5]]]
        node = Cot.get_octree(meshes, [[0, 4], [0, 4], [0, 4]], 1)
        self.assertEqual(1, len(node.Meshes))
        self.assertEqual(4, node.Size)
        self.assertEqual([0, 0, 0], node.Coordinate)
        self.assertEqual([2.0, 2.0, 2.0], node.BoundingBox)

    def test_coordinates(self):
        meshes = [[[1, 1, 1], [1, 1.5, 1], [1, 1, 1.5]]]
        node = Cot.get_octree(meshes, [[-1, 4], [-1, 4], [1, 4]], 1)
        self.assertEqual([-1, -1, 1], node.Coordinate)

    def test_size(self):
        meshes = [[[1, 1, 1], [1, 1.5, 1], [1, 1, 1.5]]]
        node = Cot.get_octree(meshes, [[-1, 0], [-2, -1], [1, 4]], 1)
        self.assertEqual(3, node.Size)

    def test_create_3_lvl_tree(self):
        meshes = [[[0.5, 0.5, 0.5], [1, 0.5, 1], [1, 1, 1]], [[0.6, 0.6, 0.6], [0.6, 0.7, 0.7], [0.5, 0.5, 0.5]]]
        node = Cot.get_octree(meshes, [[0, 4], [0, 4], [0, 4]], 0.5)
        self.assertEqual(1, len(node.Children[7].Meshes))
        self.assertEqual(1, len(node.Children[7].Children[7].Meshes))


if __name__ == '__main__':
    unittest.main()
