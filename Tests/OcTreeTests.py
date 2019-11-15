import unittest
from Experiments import OcTree


def get_empty_node_with_empty_children(size=1.0):
    res = OcTree.Node(None, size, [0, 0, 0], [])
    res.add_children()
    return res


class TestsForFindChildAndAddMesh(unittest.TestCase):

    def get_empty_node_with_empty_children(self, size: float):
        res = OcTree.Node(None, size, [0, 0, 0], [])
        res.add_children()
        return res

    def test_1(self):
        node = self.get_empty_node_with_empty_children(4)
        OcTree._find_child_and_add_mesh([1, 1, 1], 1, node)
        self.assertEqual(1, node.Children[0].Meshes[0])

    def test_2(self):
        node = self.get_empty_node_with_empty_children(4)
        OcTree._find_child_and_add_mesh([1, 1, -1], 1, node)
        self.assertEqual(1, node.Children[1].Meshes[0])

    def test_3(self):
        node = self.get_empty_node_with_empty_children(4)
        OcTree._find_child_and_add_mesh([1, -1, 1], 1, node)
        self.assertEqual(1, node.Children[2].Meshes[0])

    def test_4(self):
        node = self.get_empty_node_with_empty_children(4)
        OcTree._find_child_and_add_mesh([1, -1, -1], 1, node)
        self.assertEqual(1, node.Children[3].Meshes[0])

    def test_5(self):
        node = self.get_empty_node_with_empty_children(4)
        OcTree._find_child_and_add_mesh([-1, 1, 1], 1, node)
        self.assertEqual(1, node.Children[4].Meshes[0])

    def test_6(self):
        node = self.get_empty_node_with_empty_children(4)
        OcTree._find_child_and_add_mesh([-1, -1, 1], 1, node)
        self.assertEqual(1, node.Children[5].Meshes[0])

    def test_7(self):
        node = self.get_empty_node_with_empty_children(4)
        OcTree._find_child_and_add_mesh([-1, 1, -1], 1, node)
        self.assertEqual(1, node.Children[6].Meshes[0])

    def test_8(self):
        node = self.get_empty_node_with_empty_children(4)
        OcTree._find_child_and_add_mesh([-1, -1, -1], 1, node)
        self.assertEqual(1, node.Children[7].Meshes[0])


class TestsGetBoundingBox(unittest.TestCase):

    def test_3_point_mesh(self):
        node = get_empty_node_with_empty_children(4.5)
        mesh = [[0.5, 0.5, 0.5], [1, 1, 1], [1.5, 1.5, 1.5]]
        res = OcTree._get_bounding_box_for_mesh(mesh, node)
        self.assertEqual([[-1, -1, -1] for i in range(3)], res)

    def test_3_point_with_extreme_point(self):
        node = get_empty_node_with_empty_children(4)
        mesh = [[0, 0, 0], [1, 1, 1], [1.5, 1.5, 1.5]]
        res = OcTree._get_bounding_box_for_mesh(mesh, node)
        self.assertEqual([[-1, -1, -1] for i in range(3)], res)

    def test_3_point_mesh_one_on_bounding_boxes(self):
        node = get_empty_node_with_empty_children(4)
        mesh = [[0.5, 0.5, 0.5], [1, 1, 1], [2, 2, 2]]
        res = OcTree._get_bounding_box_for_mesh(mesh, node)
        self.assertEqual([[-1, -1, -1], [-1, -1, -1], [0, 0, 0]], res)

    def test_4_points_mesh(self):
        node = get_empty_node_with_empty_children(4)
        mesh = [[0.5, 0.5, 0.5], [0.7, 0.7, 0.7], [1, 1, 1], [1.5, 1.5, 1.5]]
        res = OcTree._get_bounding_box_for_mesh(mesh, node)
        self.assertEqual([[-1, -1, -1] for i in range(4)], res)

    def test_4_points_mesh_on_boundeng_boxes(self):
        node = get_empty_node_with_empty_children(4)
        mesh = [[0, 0, 0], [2, 0, 0], [2, 2, 2], [0, 2, 2]]
        res = OcTree._get_bounding_box_for_mesh(mesh, node)
        self.assertEqual([[-1, -1, -1], [0, -1, -1], [0, 0, 0], [-1, 0, 0]], res)


class TestedGetAllVoxelsVertex(unittest.TestCase):

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


if __name__ == "__main__":
    unittest.main()