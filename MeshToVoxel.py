from Crossing import crossing as _crossing
import ReadObj
import OcTree.CreateOcTree as Octree


def get_voxel_model(model, size_mod, size_voxel):
    """

    :param model:
    :param size_mod: [[min_x, max_x], [min_y, max_y], [min_z, max_z]]
    :param size_voxel:
    :return:
    """

    octree = Octree.get_octree(model, size_mod, size_voxel)

    res = []
    z = size_mod[2][0]
    while z < size_mod[2][1]:
        y = size_mod[1][0]
        while y < size_mod[1][1]:
            x = size_mod[0][0]
            while x < size_mod[0][1]:
                if octree.check_crossing([x, y, z], size_voxel):
                    yield [x, y, z]
                    #res.append([x, y, z])
                    # TODO Временно
                    #print([x, y, z])
                x += size_voxel
            y += size_voxel
        z += size_voxel
    return res
