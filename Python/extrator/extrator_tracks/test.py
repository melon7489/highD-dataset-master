import pandas as pd

df = pd.DataFrame({'a':[3, 3, 3, 3, 1, 1, 1, 2, 2, 2]})
print(df[df['a'] > 1]['a'].count())

# dfById = df.groupby('a', sort=False)
# for a, dfa in dfById:
#     print(dfa.count())

# 加载轨迹数据
tracksDf = pd.read_csv("../../data/60_tracks.csv", header=0)
changeOneTrackDf = tracksDf[tracksDf['id'] == 46]
track = changeOneTrackDf[(changeOneTrackDf['frame'] >= 366) & (changeOneTrackDf['frame'] <= 615)]
print(track)
