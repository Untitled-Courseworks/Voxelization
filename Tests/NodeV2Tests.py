import unittest
from OcTreeV2.NodeOcTreeV2 import Node


class TestsCreate(unittest.TestCase):

    def test_simple(self):
        node = Node(None, 4, [0, 0, 0], [1], False)
        self.assertTrue(True)


if __name__ == '__main':
    unittest.main()
