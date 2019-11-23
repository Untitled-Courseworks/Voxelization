from OcTreeV2.OcTree import Octree


def get_voxel_model(model, size_mod, size_voxel):
    """

    :param model:
    :param size_mod: [[min_x, max_x], [min_y, max_y], [min_z, max_z]]
    :param size_voxel:
    :return:
    """
    max_size_model = max(*[i[1] - i[0] for i in size_mod])
    start_pos = [i[0] for i in size_mod]
    voxels = Octree.get_all_voxels(start_pos, size_voxel, max_size_model)
    tree = Octree(voxels, size_voxel, size_mod, True)
    tree.fill_tree()
    for mesh in model:
        temp = tree.get_all_crossing(mesh, tree.Start)
        for i in temp:
            yield i
