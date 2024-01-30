import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# 创建画布
fig, axes = plt.subplots(nrows=5, ncols=5)
axList = axes.flatten()

# 翻转y轴
for ax in axList:
    ax.invert_yaxis()
    

# 加载轨迹数据
tracksDf = pd.read_csv("../../data/60_tracks2vehicle.csv", header=0)
# 加载轨迹元数据
tracksMetaDf = pd.read_csv("../../data/60_tracksMeta.csv", header=0)
# print(tracksDf.head())

# 根据 'groupId' 列进行分组
groupedTracksDf = tracksDf.groupby('groupId')

# 遍历每一组数据
for groupName, groupData in groupedTracksDf:
    # 只画前25个
    if groupName > 25:
        break
    ax = axList[groupName - 1]
    # 根据是否是主车进行分组
    oneData = groupData.groupby('egoVehicle')
    for isEgoVehicle, data in oneData:
        tracksMetaDfById = tracksMetaDf[tracksMetaDf['id'] == data['id'].values[0]]
        drivingDirection = '→' if tracksMetaDfById['drivingDirection'].values[0] == 2 else '←'
        label = 'egoVehicle' if isEgoVehicle == 1 else 'noEgoVehicle'
        color = 'red' if isEgoVehicle == 1 else 'green'
        ax.plot(data['x'], data['y'], color=color, marker='.', markersize=1, linewidth = 1)
        # ax.plot(data['x'], data['y'], color=color, marker='.', label=str(data['id'].values[0]) + drivingDirection, markersize=1, linewidth = 1)
        # ax.legend()

plt.tight_layout(pad=0.)
plt.show()