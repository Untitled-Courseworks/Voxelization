import unittest
import Crossing as Cr


class TestsGetAllProjections(unittest.TestCase):

    def test_simple(self):
        voxel = [1, 2, 3]
        res = Cr.get_all_projections([voxel], 1)
        self.assertEqual([[[1, 2]], [[1, 3]], [[2, 3]]], res)

    def test_mesh_projections(self):
        mesh = [[1, 2, 3], [3, 4, 5], [5, 6, 7], []]
        res = Cr.get_all_projections(mesh, 3)
        self.assertEqual([[[1, 2], [3, 4], [5, 6]], [[1, 3], [3, 5], [5, 7]], [[2, 3], [4, 5], [6, 7]]], res)


class TestsCheckMeshInVoxel(unittest.TestCase):

    def test_mesh_in_voxel(self):
        mesh = [[1, 1], [3, 1], [2, 3]]
        voxel = [0, 0]
        res = Cr.check_mesh_in_voxel(mesh, voxel, 4)
        self.assertTrue(res)

    def test_mesh_on_scope_voxel(self):
        voxel = [0, 0]
        mesh = [0, 1], [4, 1], [2, 4]
        res = Cr.check_mesh_in_voxel(mesh, voxel, 4)
        self.assertTrue(res)

    def test_one_vertex_in_voxel(self):
        voxel = [0, 0]
        mesh = [[3, 1], [5, 1], [5, 2]]
        res = Cr.check_mesh_in_voxel(mesh, voxel, 4)
        self.assertTrue(res)

    def test_one_vertex_on_scope_voxel(self):
        voxel = [0, 0]
        mesh = [[4, 1], [5, 0], [5, 2]]
        res = Cr.check_mesh_in_voxel(mesh, voxel, 4)
        self.assertTrue(res)

    def test_vertex_mesh_on_vertex_voxel(self):
        voxel = [0, 0]
        mesh = [[4, 0], [5, 0], [5, 2]]
        res = Cr.check_mesh_in_voxel(mesh, voxel, 4)
        self.assertTrue(res)

    def test_mesh_outside_voxel(self):
        voxel = [0, 0]
        mesh = [[4, 0], [5, 0], [5, 2]]
        res = Cr.check_mesh_in_voxel(mesh, voxel, 1)
        self.assertFalse(res)

    def test_voxel_in_mesh(self):
        mesh = [[0, 0], [5, 0], [2, 4]]
        voxel = [2, 1]
        res = Cr.check_mesh_in_voxel(mesh, voxel, 1)
        self.assertFalse(res)

    def test_vertex_voxel_on_scope_mesh(self):
        mesh = [[0, 0], [5, 0], [2, 4]]
        voxel = [1, 1]
        res = Cr.check_mesh_in_voxel(mesh, voxel, 1)
        self.assertFalse(res)


class TestsCheckVoxelInMesh(unittest.TestCase):

    def test_simple(self):
        mesh = [[0, 0], [5, 0], [2, 4]]
        voxel = [2, 1]
        res = Cr.check_voxel_in_mesh(mesh, voxel, 1)
        self.assertTrue(res)

    def test_vertex_voxel_on_scope_mesh(self):
        mesh = [[0, 0], [5, 0], [2, 4]]
        voxel = [1, 1]
        res = Cr.check_voxel_in_mesh(mesh, voxel, 1)
        self.assertTrue(res)

    def test_one_vertex_outside_mesh(self):
        mesh = [[0, 0], [5, 0], [2, 4]]
        voxel = [0, 0]
        res = Cr.check_voxel_in_mesh(mesh, voxel, 1)
        self.assertTrue(res)

    def test_one_vertex_voxel_in_mesh(self):
        mesh = [[0, 0], [5, 0], [2, 4]]
        voxel = [4, 1]
        res = Cr.check_voxel_in_mesh(mesh, voxel, 1)
        self.assertTrue(res)

    def test_vertex_voxel_on_vertex_mesh(self):
        mesh = [[0, 0], [5, 0], [2, 4]]
        voxel = [5, 0]
        res = Cr.check_voxel_in_mesh(mesh, voxel, 1)
        self.assertTrue(res)

    def test_zero_vertex_in_mesh_but_crossing(self):
        # TODO
        #  Какого хера?!
        mesh = [[0, 0], [5, 0], [2, 4]]
        voxel = [0, 3]
        res = Cr.check_voxel_in_mesh(mesh, voxel, 4)
        self.assertFalse(res)


if __name__ == '__main__':
    unittest.main()
