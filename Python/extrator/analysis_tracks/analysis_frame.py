# 分析轨迹元数据，看看总帧数的分布，选取合适的帧数作为最后的数据的帧数
# 是的，你可以使用统计学的手段来分析车辆轨迹数据的分布，并选择一个合适的总帧数。以下是一种可能的方法：

# 1. **数据探索:**
#    - 绘制直方图或核密度图，以了解每辆车的总帧数分布情况。
#    - 计算平均值和中位数，了解集中趋势。

# 2. **分析数据分布:**
#    - 判断数据是否呈正态分布。你可以使用正态性检验（例如Shapiro-Wilk检验）来检查数据是否符合正态分布的假设。
#    - 如果数据不是正态分布的，考虑使用非参数统计方法。

# 3. **选择一个合适的阈值:**
#    - 如果数据近似正态分布，你可以考虑选择均值或中位数作为阈值。均值对异常值敏感，中位数相对较为稳健。
#    - 如果数据不是正态分布，可以考虑选择分位数，如25th或75th percentile。

# 4. **验证选择的阈值:**
#    - 将所选的总帧数应用于数据，并检查有多少车辆的总帧数大于或等于该值。
#    - 可以通过绘制累积分布函数（CDF）来可视化这一比例。

# 5. **调整和优化:**
#    - 如果选择的阈值导致太多或太少的车辆被包含在其中，可以根据需要进行调整。
#    - 考虑在实际应用中的目标和限制，以便找到最合适的总帧数。

# 6. **交叉验证:**
#    - 如果可能，可以考虑使用交叉验证方法，将数据集划分为训练集和测试集，然后验证所选阈值在不同数据集上的效果。

# 请注意，这只是一个基本的方法，具体的分析取决于你的数据和实际情况。在进行统计分析时，确保理解数据的特性，并在可能的情况下与领域专家合作，以确保你的分析和结论具有实际意义。
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.interpolate import interp1d

# 加载轨迹元数据
tracksMetaDf = pd.read_csv("../../data/01_tracksMeta.csv", header=0)
dataNumFrame = tracksMetaDf['numFrames']

# 获取列的均值
mean_value = dataNumFrame.mean()

# 获取列的中位数
median_value = dataNumFrame.median()

# 获取列的最小值
min_value = dataNumFrame.min()

# 获取列的最大值
max_value = dataNumFrame.max()

# 获取列的标准差
std_deviation = dataNumFrame.std()

# 分位数计算
data = dataNumFrame.values
# 中位数
mid_value = np.median(data)
# 25%分位数
_value25 = np.percentile(data, 25)
# 75%分位数
_value_75 = np.percentile(data, 75)

# 打印统计信息
print(f"均值：{mean_value}")
print(f"中位数：{median_value}")
print(f"最小值：{min_value}")
print(f"最大值：{max_value}")
print(f"标准差：{std_deviation}")
print(f"中位数: {mid_value}")
print(f"25%分位数: {_value25}")
print(f"75%分位数: {_value_75}")

fig, axes = plt.subplots(nrows=1, ncols=2)
axList = axes.flatten()

# 绘制直方图
axList[0].hist(dataNumFrame, bins=100, density=True, alpha=0.5, color='b', label='Histogram')

# 添加标签和标题
axList[0].legend()
axList[0].set_xlabel('Value')
axList[0].set_ylabel('Frequency Density')
axList[0].set_title('Histogram of Data')


# 计算数据的累积分布函数
sorted_data = np.sort(dataNumFrame)[::-1]
cumulative = np.arange(len(sorted_data)) / float(len(sorted_data))
# 绘制累积分布函数曲线
axList[1].plot(sorted_data, cumulative, label='CDF')

# 使用线性插值获得给定 x 值对应的 y 值
# 使用 interp1d 创建插值函数
cdf_interp = interp1d(sorted_data, cumulative, kind='linear', fill_value=(0, 1), bounds_error=False)

given_x = 250
given_y = cdf_interp(given_x)
print(f'given_x:{given_x},given_y:{given_y:.2f}')
# 在图上标记给定 x 值对应的点
plt.scatter(given_x, given_y, color='red', label=f'Interpolated for x={given_x}', s=10)

# 添加标签和标题
axList[1].invert_xaxis()
axList[1].legend()
axList[1].set_xlabel('Value')
axList[1].set_ylabel('Cumulative Probability')
axList[1].set_title('Cumulative Distribution Function (CDF) of Data')

fig.tight_layout()
# 显示图形
plt.show()




