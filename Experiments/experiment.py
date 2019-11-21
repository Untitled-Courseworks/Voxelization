from OcTreeV2.NodeOcTreeV2 import Node

voxels = Node._get_all_voxels_vertex([0, 0, 0], 2)
v = []
for i in voxels:
    temp = Node._get_all_voxels_vertex(i, 1)
    for t in temp:
        v.append(t)
voxels = []
for i in v:
    temp = Node._get_all_voxels_vertex(i, 0.5)
    for t in temp:
        voxels.append(t)

search = []
count = 0
for i in voxels:
    if 2 in i or 2 in [j + 0.5 for j in i]:
        count += 1
print(count)
