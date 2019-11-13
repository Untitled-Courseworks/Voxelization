import unittest
from OcTree import *


class TestsForFindChildAndAddMesh(unittest.TestCase):

    def get_empty_node_with_empty_children(self, size: float):
        res = Node(None, size, [0, 0, 0], [])
        res.add_children()
        return res

    def test_1(self):
        node = self.get_empty_node_with_empty_children(4)
        find_child_and_add_mesh([1, 1, 1], 1, node)
        self.assertEqual(1, node.Children[0].Meshes[0])

    def test_2(self):
        node = self.get_empty_node_with_empty_children(4)
        find_child_and_add_mesh([1, 1, -1], 1, node)
        self.assertEqual(1, node.Children[1].Meshes[0])

    def test_3(self):
        node = self.get_empty_node_with_empty_children(4)
        find_child_and_add_mesh([1, -1, 1], 1, node)
        self.assertEqual(1, node.Children[2].Meshes[0])

    def test_4(self):
        node = self.get_empty_node_with_empty_children(4)
        find_child_and_add_mesh([1, -1, -1], 1, node)
        self.assertEqual(1, node.Children[3].Meshes[0])

    def test_5(self):
        node = self.get_empty_node_with_empty_children(4)
        find_child_and_add_mesh([-1, 1, 1], 1, node)
        self.assertEqual(1, node.Children[4].Meshes[0])

    def test_6(self):
        node = self.get_empty_node_with_empty_children(4)
        find_child_and_add_mesh([-1, -1, 1], 1, node)
        self.assertEqual(1, node.Children[5].Meshes[0])

    def test_7(self):
        node = self.get_empty_node_with_empty_children(4)
        find_child_and_add_mesh([-1, 1, -1], 1, node)
        self.assertEqual(1, node.Children[6].Meshes[0])

    def test_8(self):
        node = self.get_empty_node_with_empty_children(4)
        find_child_and_add_mesh([-1, -1, -1], 1, node)
        self.assertEqual(1, node.Children[7].Meshes[0])


if __name__ == "__main__":
    unittest.main()