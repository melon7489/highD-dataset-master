import pandas as pd
import numpy as np 


def save_npz(i):
    # 加载轨迹数据
    tracksDf = pd.read_csv(f"../../data/{i:0>2d}_tracks2vehicle.csv", header=0)

    minX = tracksDf['x'].min()
    minY = tracksDf['y'].min()
    maxX = tracksDf['x'].max()
    maxY = tracksDf['y'].max()
    # 根据 'groupId' 列进行分组
    groupedTracksDf = tracksDf.groupby('groupId')

    # 存放每一组数据的列表
    tracksList = []
    # 遍历每一组数据
    for groupName, groupData in groupedTracksDf:
        # 存放每组数据中两车的列表
        track2List = []
        # 根据 'egoVehicle' 列进行分组
        groupData['x'] = groupData['x'] - groupData['x'].min()
        groupData['y'] = groupData['y'] - groupData['y'].min()
        groupEgoData = groupData.groupby('egoVehicle')
        for isEgo, trackData in groupEgoData:
            track2List.append(trackData[['x', 'y','xVelocity','yVelocity','xAcceleration','yAcceleration','id']].values)
        tracksList.append(track2List)
    tracksNp = np.array(tracksList)
    print(tracksNp.shape)
    return tracksNp
    

if __name__ == '__main__': 
    tracksNp = None
    for i in range(60):
        if i == 0:
            tracksNp = save_npz(i + 1)
        else:    
            tracksNp = np.concatenate([tracksNp, save_npz(i + 1)])
    np.savez(r'E:\project\benchmark_VAE\examples\data\highD\changeLane_backcaras00_60.npz', data = tracksNp)

