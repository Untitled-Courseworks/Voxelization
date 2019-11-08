import unittest
import Crossing as Cr


class TestsGetAllProjections(unittest.TestCase):

    def test_simple(self):
        voxel = [1, 2, 3]
        res = Cr._get_all_projections([voxel], 1)
        self.assertEqual([[[1, 2]], [[1, 3]], [[2, 3]]], res)

    def test_mesh_projections(self):
        mesh = [[1, 2, 3], [3, 4, 5], [5, 6, 7], []]
        res = Cr._get_all_projections(mesh, 3)
        self.assertEqual([[[1, 2], [3, 4], [5, 6]], [[1, 3], [3, 5], [5, 7]], [[2, 3], [4, 5], [6, 7]]], res)


class TestsCheckMeshInVoxel(unittest.TestCase):

    def test_mesh_in_voxel(self):
        mesh = [[1, 1], [3, 1], [2, 3]]
        voxel = [0, 0]
        res = Cr._check_mesh_in_voxel(mesh, voxel, 4)
        self.assertTrue(res)

    def test_mesh_on_scope_voxel(self):
        voxel = [0, 0]
        mesh = [0, 1], [4, 1], [2, 4]
        res = Cr._check_mesh_in_voxel(mesh, voxel, 4)
        self.assertTrue(res)

    def test_one_vertex_in_voxel(self):
        voxel = [0, 0]
        mesh = [[3, 1], [5, 1], [5, 2]]
        res = Cr._check_mesh_in_voxel(mesh, voxel, 4)
        self.assertTrue(res)

    def test_one_vertex_on_scope_voxel(self):
        voxel = [0, 0]
        mesh = [[4, 1], [5, 0], [5, 2]]
        res = Cr._check_mesh_in_voxel(mesh, voxel, 4)
        self.assertTrue(res)

    def test_mesh_outside_voxel(self):
        voxel = [0, 0]
        mesh = [[4, 0], [5, 0], [5, 2]]
        res = Cr._check_mesh_in_voxel(mesh, voxel, 1)
        self.assertFalse(res)

    def test_voxel_in_mesh(self):
        mesh = [[0, 0], [5, 0], [2, 4]]
        voxel = [2, 1]
        res = Cr._check_mesh_in_voxel(mesh, voxel, 1)
        self.assertFalse(res)

    def test_vertex_voxel_on_scope_mesh(self):
        mesh = [[0, 0], [5, 0], [2, 4]]
        voxel = [1, 1]
        res = Cr._check_mesh_in_voxel(mesh, voxel, 1)
        self.assertFalse(res)

    def test_vertex_voxel_on_vertex_mesh(self):
        mesh = [[0, 0], [5, 0], [2, 4]]
        voxel = [5, 0]
        res = Cr._check_mesh_in_voxel(mesh, voxel, 1)
        self.assertTrue(res)


class TestsCheckVoxelInMesh(unittest.TestCase):

    def test_simple(self):
        mesh = [[0, 0], [5, 0], [2, 4]]
        voxel = [2, 1]
        res = Cr._check_voxel_in_mesh(mesh, voxel, 1)
        self.assertTrue(res)

    def test_vertex_voxel_on_scope_mesh(self):
        mesh = [[0, 0], [5, 0], [2, 4]]
        voxel = [1, 1]
        res = Cr._check_voxel_in_mesh(mesh, voxel, 1)
        self.assertTrue(res)

    def test_one_vertex_outside_mesh(self):
        mesh = [[0, 0], [5, 0], [2, 4]]
        voxel = [0, 0]
        res = Cr._check_voxel_in_mesh(mesh, voxel, 1)
        self.assertTrue(res)

    def test_one_vertex_voxel_in_mesh(self):
        mesh = [[0, 0], [5, 0], [2, 4]]
        voxel = [4, 1]
        res = Cr._check_voxel_in_mesh(mesh, voxel, 1)
        self.assertTrue(res)

    def test_vertex_voxel_on_vertex_mesh(self):
        mesh = [[0, 0], [5, 0], [2, 4]]
        voxel = [5, 0]
        res = Cr._check_voxel_in_mesh(mesh, voxel, 1)
        self.assertFalse(res)

    def test_zero_vertex_in_mesh_but_crossing(self):
        mesh = [[0, 0], [5, 0], [2, 4]]
        voxel = [0, 3]
        res = Cr._check_voxel_in_mesh(mesh, voxel, 4)
        self.assertFalse(res)

    def test_two_joint_vertex(self):
        mesh = [[1, 0], [2, 0], [1, 1]]
        voxel = [0, 0]
        res = Cr._check_voxel_in_mesh(mesh, voxel, 1)
        self.assertFalse(res)


class TestsCheckCrossingLines(unittest.TestCase):

    def test_crossing_point_between_voxels_points(self):
        res = Cr._check_crossing_lines([2, 3], [2, -3], [0, 0], [4, 0])
        self.assertTrue(res)

        res = Cr._check_crossing_lines([0, 3], [4, -3], [0, 0], [4, 0])
        self.assertTrue(res)

        res = Cr._check_crossing_lines([-1, 3], [5, -3], [0, 0], [4, 0])
        self.assertTrue(res)

    def test_crossing_point_not_between_voxels_points(self):
        res = Cr._check_crossing_lines([-3, 3], [-3, -3], [0, 0], [4, 0])
        self.assertFalse(res)

        res = Cr._check_crossing_lines([-3, 3], [0, -3], [0, 0], [4, 0])
        self.assertFalse(res)

        res = Cr._check_crossing_lines([0, 2], [4, 1], [0, 0], [4, 0])
        self.assertFalse(res)

    def test_parallel(self):
        res = Cr._check_crossing_lines([0, 2], [4, 2], [0, 0], [4, 0])
        self.assertFalse(res)

        res = Cr._check_crossing_lines([-1, 2], [1, 2], [0, 0], [4, 0])
        self.assertFalse(res)

        res = Cr._check_crossing_lines([-1, 2], [5, 2], [0, 0], [4, 0])
        self.assertFalse(res)

    def test_similarity(self):
        res = Cr._check_crossing_lines([1, 0], [2, 0], [0, 0], [4, 0])
        self.assertTrue(res)

        res = Cr._check_crossing_lines([1, 0], [5, 0], [0, 0], [4, 0])
        self.assertTrue(res)

        res = Cr._check_crossing_lines([0, 0], [4, 0], [0, 0], [4, 0])
        self.assertTrue(res)

        res = Cr._check_crossing_lines([-1, 0], [4, 0], [0, 0], [4, 0])
        self.assertTrue(res)

        res = Cr._check_crossing_lines([0, 0], [5, 0], [0, 0], [4, 0])
        self.assertTrue(res)

        res = Cr._check_crossing_lines([-1, 0], [5, 0], [0, 0], [4, 0])
        self.assertFalse(res)

    def test_crossing_point_between_voxels_points_but_not_between_mesh_points(self):
        res = Cr._check_crossing_lines([2, 3], [2, 2], [0, 0], [4, 0])
        self.assertFalse(res)


class TestsCheckCrossingProjectionAndLine(unittest.TestCase):

    def test_crossing_one_point_in_voxel(self):
        voxel = [0, 0]
        ver_1 = [1, 1]
        ver_2 = [1, 3]
        res = Cr._check_crossing_projection_and_line(voxel, 2, ver_1, ver_2)
        self.assertTrue(res)

    def test_crossing_zero_point_in_mesh_line(self):
        res = Cr._check_crossing_projection_and_line([0, 0], 2, [1, 3], [1, 4])
        self.assertFalse(res)

        res = Cr._check_crossing_projection_and_line([0, 0], 2, [1, 3], [2, 4])
        self.assertFalse(res)

    def test_voxel_between_points(self):
        res = Cr._check_crossing_projection_and_line([0, 0], 2, [1, 3], [1, -2])
        self.assertTrue(res)

    def test_crossing_point_on_vertex_voxel(self):
        res = Cr._check_crossing_projection_and_line([0, 0], 2, [-1, 1], [1, 3])
        self.assertTrue(res)

    def test_line_not_crossing(self):
        res = Cr._check_crossing_projection_and_line([0, 0], 2, [0, 3], [2, 3])
        self.assertFalse(res)

    def test_similarity(self):
        res = Cr._check_crossing_projection_and_line([0, 0], 2, [0, 2], [2, 2])
        self.assertTrue(res)

        res = Cr._check_crossing_projection_and_line([0, 0], 2, [-1, 2], [3, 2])
        self.assertTrue(res)

        res = Cr._check_crossing_projection_and_line([0, 0], 2, [0.5, 2], [1, 2])
        self.assertTrue(res)


class TestsCheckCrossingProjections(unittest.TestCase):

    def test_three_mesh_points_outside_voxel(self):
        mesh = [[-1, 1], [2, 4], [4, 1]]
        res = Cr._check_crossing_projections([0, 0], 3, mesh)
        self.assertTrue(res)

        mesh = [[2, 4], [4, 2], [4, 4]]
        res = Cr._check_crossing_projections([0, 0], 3, mesh)
        self.assertTrue(res)

    def test_not_crossing(self):
        mesh = [[4, 0], [4, 1], [5, 1]]
        res = Cr._check_crossing_projections([0, 0], 3, mesh)
        self.assertFalse(res)

        mesh = [[7, 0], [4, 0], [4, 2]]
        res = Cr._check_crossing_projections([0, 0], 3, mesh)
        self.assertFalse(res)

        mesh = [[7, 0], [4, 0], [4, 4]]
        res = Cr._check_crossing_projections([0, 0], 3, mesh)
        self.assertFalse(res)

    def test_mesh_is_line(self):
        mesh = [[0, 0], [2, 2], [0, 0]]
        res = Cr._check_crossing_projections([0, 0], 3, mesh)
        self.assertTrue(res)

        mesh = [[4, 0], [4, 1], [4, 0]]
        res = Cr._check_crossing_projections([0, 0], 3, mesh)
        self.assertFalse(res)

    def test_mesh_points_on_voxel_vertex(self):
        mesh = [[0, 0], [3, 0], [0, 3]]
        res = Cr._check_crossing_projections([0, 0], 3, mesh)
        self.assertTrue(res)

    def test_edge_voxel_and_mesh_is_conside(self):
        mesh = [[-1, 3], [4, 3], [2, 5]]
        res = Cr._check_crossing_projections([0, 0], 3, mesh)
        self.assertTrue(res)

    def test_mesh_in_voxel(self):
        mesh = [[1, 1], [2, 1], [1, 2]]
        res = Cr._check_crossing_projections([0, 0], 3, mesh)
        self.assertFalse(res)

        mesh = [[1, 1], [2, 2], [1, 1]]
        res = Cr._check_crossing_projections([0, 0], 3, mesh)
        self.assertFalse(res)

    def test_voxel_in_mesh(self):
        mesh = [[0, 0], [0, 5], [5, 0]]
        res = Cr._check_crossing_projections([1, 1], 1, mesh)
        self.assertFalse(res)


class TestsCheckAll(unittest.TestCase):

    def test_three_mesh_points_outside_voxel(self):
        mesh = [[-1, 1], [2, 4], [4, 1]]
        res = Cr._check_all(mesh, [0, 0], 3)
        self.assertTrue(res)

        mesh = [[2, 4], [4, 2], [4, 4]]
        res = Cr._check_all(mesh, [0, 0], 3)
        self.assertTrue(res)

    def test_not_crossing(self):
        mesh = [[4, 0], [4, 1], [5, 1]]
        res = Cr._check_all(mesh, [0, 0], 3)
        self.assertFalse(res)

        mesh = [[7, 0], [4, 0], [4, 2]]
        res = Cr._check_all(mesh, [0, 0], 3)
        self.assertFalse(res)

        mesh = [[7, 0], [4, 0], [4, 4]]
        res = Cr._check_all(mesh, [0, 0], 3)
        self.assertFalse(res)

    def test_mesh_is_line(self):
        mesh = [[0, 0], [2, 2], [0, 0]]
        res = Cr._check_all(mesh, [0, 0], 3)
        self.assertTrue(res)

        mesh = [[4, 0], [4, 1], [4, 0]]
        res = Cr._check_all(mesh, [0, 0], 3)
        self.assertFalse(res)

    def test_mesh_points_on_voxel_vertex(self):
        mesh = [[0, 0], [3, 0], [0, 3]]
        res = Cr._check_all(mesh, [0, 0], 3)
        self.assertTrue(res)

    def test_edge_voxel_and_mesh_is_conside(self):
        mesh = [[-1, 3], [4, 3], [2, 5]]
        res = Cr._check_all(mesh, [0, 0], 3)
        self.assertTrue(res)

    def test_mesh_in_voxel(self):
        mesh = [[1, 1], [2, 1], [1, 2]]
        res = Cr._check_all(mesh, [0, 0], 3)
        self.assertTrue(res)

        mesh = [[1, 1], [2, 2], [1, 1]]
        res = Cr._check_all(mesh, [0, 0], 3)
        self.assertTrue(res)

    def test_voxel_in_mesh(self):
        mesh = [[0, 0], [0, 5], [5, 0]]
        res = Cr._check_all(mesh, [1, 1], 1)
        self.assertTrue(res)

class TestsCrossing(unittest.TestCase):
    # TODO
    pass


if __name__ == '__main__':
    unittest.main()
