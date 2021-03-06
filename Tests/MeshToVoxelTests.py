import Visualization
import MeshToVoxel as MV
import unittest
from Tests import Samples
import ReadObj
from Visual_2_0 import ShowModel


class TestsMeshToVoxel(unittest.TestCase):

    def test_1(self):
        mod = ReadObj.read_file("deer.obj")
        #file = open("deer.obj")

        Visualization.get_model(mod)

    def test_triangle(self):
        triangle = Samples.triangle()
        size_model = [3, 3, 1]
        answ = [[0, 0, 0], [1, 0, 0], [0, 1, 0], [1, 1, 0], [2, 1, 0], [0, 2, 0], [1, 2, 0], [2, 2, 0]]
        res = MV.get_voxel_model(triangle, size_model, 1)
        #Visualization.get_model(res)
        #Visualization.get_model(answ)
        for i in range(len(answ)):
            self.assertTrue(answ[i] == res[i] )


    def test_cube(self):
        # TODO Неверный пример куба
        cube = Samples.cube()
        size_model = Samples.find_size_model(cube)
        voxel_cube = [i for i in MV.get_voxel_model(cube, [[0, 3], [0, 3], [0, 3]], 2)]
        ShowModel(voxel_cube, 2, [[0, 0, 0], [3, 3, 3]], False)
        #self.print_in_file(voxel_cube)
        #Visualization.get_model(voxel_cube, 0.1)
        #objects = [[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 1, 1], [1, 0, 0], [1, 0, 1], [1, 1, 0], [1, 1, 1]]
        #Visualization.get_model(objects)
        #answ = []
        #for z in range(3):
         #   for y in range(3):
          #      for x in range(3):
           #         answ.append([x, y, z])
        #for i in range(len(answ)):
         #   self.assertEqual(answ[i], voxel_cube[i], str(answ[i]))

    def test_pyramid(self):
        # TODO Ошибка объявления начальных вокселей
        pyramid = Samples.pyramid2()
        model = [i for i in MV.get_voxel_model(pyramid, [[0, 4], [0, 4], [0, 4]], 0.1)]
        self.print_in_file(model)
        #Visualization.get_model(model)
        #ShowModel(model, 0.1, True)

    def print_in_file(self, voxels: []):
        with open("Voxels.txt", "w") as file:
            file.write("[")
            for i in voxels:
                file.write("[")
                file.write(str(i[0]) + ", ")
                file.write(str(i[1]) + ", ")
                file.write(str(i[2]))
                file.write("],")
                file.write("\n")
            file.write("]")


if __name__ == '__main__':
    unittest.main()
