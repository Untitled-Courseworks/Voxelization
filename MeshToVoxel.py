import math
from Crossing import crossing as _crossing
import Visualization


def get_voxel_model(model, size_mod, size_voxel):
    res = []
    for z in range(math.ceil(size_mod[2] / size_voxel)):
        for y in range(math.ceil(size_mod[1] / size_voxel)):
            for x in range(math.ceil(size_mod[0] / size_voxel)):
                for m in model:
                    if _crossing(m, [x, y, z], size_voxel):
                        res.append([x, y, z])
                        break
    return res