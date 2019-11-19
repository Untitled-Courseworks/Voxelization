from OcTreeV2.NodeOcTreeV2 import Node


class Octree:

    def __init__(self, objects: [], size_voxel: [], ep: [], is_voxel: bool):
        max_size_model = max(*[i[1] - i[0] for i in ep])
        self.Start = Node(None, max_size_model, [point[0] for point in ep], is_voxel)
        self.Start.add_objects(objects)
        self.Size_voxel = size_voxel
        self.Start.fill_tree(self.Size_voxel)

    def crossing_with_meshes(self):

