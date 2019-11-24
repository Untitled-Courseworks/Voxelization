import MeshToVoxel
import ReadObj
import Visualization


path = "experiments/sphere.obj"
size_voxel = 0.1
model = ReadObj.read_file(path)
voxels = MeshToVoxel.get_voxel_model(model[0], model[1], size_voxel)
Visualization.get_model(voxels, size_voxel)
