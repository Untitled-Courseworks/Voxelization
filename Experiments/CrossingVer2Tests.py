import unittest
from Experiments import CrossingVer2 as Cr


class TestsPointInTriangle(unittest.TestCase):
    # Точно рабочий, но если есть желание - можно написать пару тестов
    pass


class TestsGetAllProjections(unittest.TestCase):

    def test_simple(self):
        voxel = [1, 2, 3]
        res = Cr._get_all_projections([voxel], 1)
        self.assertEqual([[[1, 2]], [[1, 3]], [[2, 3]]], res)

    def test_mesh_projections(self):
        mesh = [[1, 2, 3], [3, 4, 5], [5, 6, 7], []]
        res = Cr._get_all_projections(mesh, 3)
        self.assertEqual([[[1, 2], [3, 4], [5, 6]], [[1, 3], [3, 5], [5, 7]], [[2, 3], [4, 5], [6, 7]]], res)


class TestGetCoefficientPlane(unittest.TestCase):

    def test_mesh_is_line(self):
        mesh = [[1, 0, 0], [0, 1, 1], [0, 1, 1]]
        res = Cr._get_coefficients_plane(*mesh)
        self.assertTrue(res)


if __name__ == '__main__':
    unittest.main()