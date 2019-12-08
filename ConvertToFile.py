from OcTreeV2.NodeOcTreeV2 import Node


def convert(voxels: [], size_voxel: float):
    points = get_all_points(voxels, size_voxel)
    with open("model.PCD", "w") as file:
        write_header(file, len(points))
        for point in points:
            file.write(get_str_from_point(point))


def write_header(file, count_points: int):
    file.write("# .PCD v.7 - Point Cloud Data file format\n")
    file.write("VERSION .7\n")
    file.write("FIELDS x y z\n")
    file.write("SIZE 4 4 4 4\n")
    file.write("TYPE F F F F\n")
    file.write("COUNT 1 1 1 1\n")
    file.write("WIDTH 213\n")
    file.write("HEIGHT 1\n")
    file.write("VIEWPOINT 0 0 0 1 0 0 0\n")
    file.write("POINTS " + str(count_points))
    file.write("DATA ascii")


def get_all_points(voxels: [], size: int):
    res = []
    for i in voxels:
        [res.append(j) for j in Node.get_all_voxels_vertex(i, size)]
    return res


def get_str_from_point(point: []):
    return str(point[0]) + " " + str(point[1]) + " " + str(point[2])
