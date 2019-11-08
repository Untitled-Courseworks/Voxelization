import MeshToVoxel as MV
import unittest
import Visualization
from Tests import Samples


class TestsMeshToVoxel(unittest.TestCase):

    def test_cube(self):
        cube = Samples.cube()
        size_model = Samples.find_size_model(cube)
        voxel_cube = MV.get_voxel_model(cube, size_model, 1)
        answ = []
        for z in range(3):
            for y in range(3):
                for x in range(3):
                    answ.append([x, y, z])
        for i in range(len(answ)):
            self.assertEqual(answ[i], voxel_cube[i], str(answ[i]))


if __name__ == '__main__':
    unittest.main()