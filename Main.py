import MeshToVoxel
import ReadObj
import Visualization
import Visual_2_0


path = "experiments/sphere.obj"
size_voxel = 0.3
model = ReadObj.read_file(path)

voxels = MeshToVoxel.get_voxel_model(model[0], model[1], size_voxel)

Visual_2_0.ShowModel(voxels, size_voxel, [[i[0] for i in model[1]], [i[1] for i in model[1]]], True)
