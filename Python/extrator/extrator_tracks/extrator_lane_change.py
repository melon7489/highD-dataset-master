import pandas as pd

def extrator(i):
    # 加载轨迹数据
    tracksDf = pd.read_csv(f"../../data/{i:0>2d}_tracks.csv", header=0)
    # 加载轨迹元数据
    tracksMetaDf = pd.read_csv(f"../../data/{i:0>2d}_tracksMeta.csv", header=0)
    # 使用布尔索引提取numsChange列中值为1的数据，先提取方向全是向右的。
    changeOneMetaDf = tracksMetaDf[(tracksMetaDf['numLaneChanges'] == 1) & (tracksMetaDf['drivingDirection'] == 2)]
    # 提取换道数为1的轨迹id
    changeOneMetaDfIds = changeOneMetaDf["id"]
    # print(changeOneMetaDfId.head())

    # 对数据分组，两车交互为一组
    count = 1

    # 新建文件存放提取出的两车交互轨迹分组的结果
    tracks2vehiclePath = f"../../data/{i:0>2d}_tracks2vehicle.csv"
    # 写入表头
    df = pd.DataFrame(columns = list(tracksDf.columns) + ['egoVehicle'] + ['groupId'])
    df.to_csv(tracks2vehiclePath, index=False, header=True)

    # 提取换道数为1的轨迹数据
    for changeOneMetaDfId in changeOneMetaDfIds:
        
        # 查找对应id的Meta数据 
        egoChangeOneTrackMetaDf = changeOneMetaDf[changeOneMetaDf["id"] == changeOneMetaDfId]
        egoInitialFrame = egoChangeOneTrackMetaDf['initialFrame']
        egoFinalFrame = egoChangeOneTrackMetaDf['finalFrame']
        # 剔除掉主车帧数小于250的轨迹
        if egoChangeOneTrackMetaDf['numFrames'].values < 250:
            # print('主车', egoChangeOneTrackMetaDf['numFrames'].values)
            continue

        # 查找对应id的tracks数据
        changeOneTrackDf = tracksDf[tracksDf["id"] == changeOneMetaDfId]
        changeOneTrackDf['egoVehicle'] = 1

        # 查找laneId改变的那两帧的临界帧,对应的两行数据
        laneIds = changeOneTrackDf["laneId"].values #[88888888888777777777]
        for i in range(len(laneIds) - 1):
            # print(laneIds[i],"   ",laneIds[i + 1])
            if laneIds[i] != laneIds[i + 1]:
                preFrameDf = changeOneTrackDf.iloc[i]
                afterFrameDf = changeOneTrackDf.iloc[i + 1]
                # print("preFrameDf", preFrameDf["laneId"])
                # print("afterFrameDf", afterFrameDf["laneId"])
                # 分别找变道前 前车、后车 变道后 前车、后车的轨迹数据
                prePrecedingIdTracks =  tracksDf[tracksDf["id"] == preFrameDf["precedingId"]] if preFrameDf["precedingId"] != 0 else None
                preFollowingIdTracks = tracksDf[tracksDf["id"] == preFrameDf["followingId"]] if preFrameDf["followingId"] != 0 else None
                afPrecedingIdTracks = tracksDf[tracksDf["id"] == afterFrameDf["precedingId"]] if afterFrameDf["precedingId"] != 0 else None
                afFollowingIdTracks = tracksDf[tracksDf["id"] == afterFrameDf["followingId"]] if afterFrameDf["followingId"] != 0 else None
                # 分组提取
                for eachLocationTracks in [prePrecedingIdTracks, preFollowingIdTracks, afPrecedingIdTracks, afFollowingIdTracks]:
                    if eachLocationTracks is not None:
                        # 查找对应id的Meta数据 
                        noegoTrackMetaDf = tracksMetaDf[tracksMetaDf["id"] == eachLocationTracks['id'].values[0]]
                        noegoInitialFrame = noegoTrackMetaDf['initialFrame']
                        noegoFinalFrame = noegoTrackMetaDf['finalFrame']
                        # 剔除掉两者同时开始同时结束的帧小于250的轨迹
                        initialFrame = max(egoInitialFrame.values, noegoInitialFrame.values)[0]
                        finalFrame = min(egoFinalFrame.values, noegoFinalFrame.values)[0]
                        if (finalFrame - initialFrame) < 250:
                            # print('同时', (finalFrame - initialFrame))
                            continue
                        # 经过上一步的剔除，留下来的主车轨迹可能就没有变道行为了（因为对主车和非主车的帧数取了个交集）因此需要剔除
                        if (preFrameDf['frame'] < initialFrame) or (afterFrameDf['frame'] > finalFrame):
                            # print('相交', eachLocationTracks['id'].values[0])
                            continue

                        # 最后筛选相同大小的250段帧
                        '''
                        - 之后的判定操作要在min_finalFrame-max_initialFrame之间
                        - 对ego-vehicle数据groupby("laneId")分组之后，对两半数据进行提取：
                            - 变道前帧数 >= 125 帧 && 变道后帧数 >= 125帧：则提取ego-vehicle的变道前125帧+变道后125帧；
                                no-ego-vehicle的帧号与ego-vehicle保持一致。
                            - 变道前帧数 >= 125 帧 && 变道后帧数 < 125帧：则提取ego-vehicle的变道后所有帧+变道前（250-变道后所有帧）帧；
                                no-ego-vehicle的帧号与ego-vehicle保持一致。
                            - 变道前帧数 < 125 帧 && 变道后帧数 >= 125帧：则提取ego-vehicle的变道前所有帧+变道后（250-变道前所有帧）帧；
                                no-ego-vehicle的帧号与ego-vehicle保持一致。
                        '''
                        # 提取ego-vehicle介于min_finalFrame-max_initialFrame之间的轨迹个数

                        preTrackCount = preFrameDf['frame'] - initialFrame + 1
                        afterTrackCount = finalFrame - afterFrameDf['frame'] + 1

                        # print("fin - ini", finalFrame - initialFrame + 1)
                        # print('pre + after',preTrackCount + afterTrackCount)

                        # - 变道前帧数 >= 125 帧 && 变道后帧数 >= 125帧：则提取ego-vehicle的变道前125帧+变道后125帧；
                        #     no-ego-vehicle的帧号与ego-vehicle保持一致。
                        if (preTrackCount >= 125) and (afterTrackCount >= 125):
                            initialFrame = preFrameDf['frame'] - 125 + 1
                            finalFrame = afterFrameDf['frame'] + 125 - 1
                            # print('变道前帧数 >= 125 帧 && 变道后帧数 >= 125帧:', finalFrame - initialFrame + 1)

                        # - 变道前帧数 >= 125 帧 && 变道后帧数 < 125帧：则提取ego-vehicle的变道后所有帧+变道前（250-变道后所有帧）帧；
                        #     no-ego-vehicle的帧号与ego-vehicle保持一致。
                        elif (preTrackCount >= 125) and (afterTrackCount < 125):
                            finalFrame = finalFrame
                            initialFrame = finalFrame - 250 + 1
                            # print('变道前帧数 >= 125 帧 && 变道后帧数 < 125帧:', finalFrame - initialFrame + 1)

                        # - 变道前帧数 < 125 帧 && 变道后帧数 >= 125帧：则提取ego-vehicle的变道前所有帧+变道后（250-变道前所有帧）帧；
                        #     no-ego-vehicle的帧号与ego-vehicle保持一致。
                        elif (preTrackCount < 125) and (afterTrackCount >= 125):
                            initialFrame = initialFrame
                            finalFrame = initialFrame + 250 - 1
                            # print('变道前帧数 < 125 帧 && 变道后帧数 >= 125帧:', finalFrame - initialFrame + 1)
                            
                        else:
                            continue
                        print('initialFrame', initialFrame, 'finalFrame', finalFrame)
                        finialEgoTrack = changeOneTrackDf[(changeOneTrackDf['frame'] >= initialFrame) & (changeOneTrackDf['frame'] <= finalFrame)]
                        eachLocationTracks = eachLocationTracks[(eachLocationTracks['frame'] >= initialFrame) & (eachLocationTracks['frame'] <= finalFrame)]
                        print('finialEgoTrack', finialEgoTrack['frame'].count())
                        print('eachLocationTracks', eachLocationTracks['frame'].count())
                        eachLocationTracks['egoVehicle'] = 0
                        eachLocationFrames = [finialEgoTrack, eachLocationTracks]
                        eachLocationResult = pd.concat(eachLocationFrames)
                        eachLocationResult["groupId"] = count
                        count += 1
                        print(eachLocationResult.tail())
                        eachLocationResult.to_csv(tracks2vehiclePath, mode='a', index=False, header=False) 
                break 


if __name__ == '__main__':    
    for i in range(60):
        extrator(i + 1)

