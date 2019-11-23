import MeshToVoxel
import ReadObj
import Visualization


path = "experiments/deer.obj"
size_voxel = 1.0
model = ReadObj.read_file(path)
voxels = MeshToVoxel.get_voxel_model(model[0], model[1], size_voxel)
Visualization.get_model(voxels, size_voxel)
