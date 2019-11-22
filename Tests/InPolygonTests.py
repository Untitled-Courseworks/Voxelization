from Experiments.experiment import in_polygon
import unittest


class TestsInPolygon(unittest.TestCase):

    def get_x_and_y(self, figure):
        res = [[], []]
        for i in range(len(figure)):
            res[0].append(figure[i][0])
            res[1].append(figure[i][1])
        return res

    def test_point_in_triangle(self):
        triangle = [[0, 0], [4, 0], [2, 4]]
        x_y = self.get_x_and_y(triangle)
        res = in_polygon(triangle, [0, 0])
        self.assertEqual(0, res)
        res = in_polygon(1, 0, x_y[0], x_y[1])
        self.assertEqual(1, res)
        res = in_polygon(1, 2, x_y[0], x_y[1])
        self.assertEqual(1, res)
        res = in_polygon(0, 2, x_y[0], x_y[1])
        self.assertEqual(0, res)

    def test_point_in_sqare(self):
        sqare = [[0, 0], [4, 0], [4, 4], [0, 4]]
        x_y = self.get_x_and_y(sqare)
        res = in_polygon(1, 1, x_y[0], x_y[1])
        self.assertEqual(1, res)
        res = in_polygon(4, 0, x_y[0], x_y[1])


if __name__ == '__main__':
    unittest.main()

