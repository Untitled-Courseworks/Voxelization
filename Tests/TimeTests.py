import time
import Tests.Samples as Samples
from OcTreeV2.OcTree import Octree
import MeshToVoxel
import Visualization


model = Samples.pyramid2()

start_time = time.time()
voxels = Octree.get_all_voxels([0, 0, 0], 0.1, 4)
tree = Octree(voxels, 0.1, [[0, 4], [0, 4], [0, 4]], True)
tree.fill_tree()
voxels = []
for i in model:
    for j in tree.get_all_crossing(i, tree.Start):
        voxels.append(j)
print(print("--- %s seconds ---" % (time.time() - start_time)))

start_time = time.time()
voxels = [i for i in MeshToVoxel.get_voxel_model(model, [[0, 4], [0, 4], [0, 4]], 0.1)]
print("--- %s seconds ---" % (time.time() - start_time))
