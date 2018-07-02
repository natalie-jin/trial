import pandas
import matplotlib.pyplot as plt
import numpy
import os

df = pandas.read_csv('000002_资产负债表.csv', index_col=0)
di = pandas.read_csv('000002_利润表.csv', index_col=0)
df = df.T
df['计算总资产'] = df['所有者权益(或股东权益)合计(万元)'] + df['负债合计(万元)']

m = map(lambda x, y: x == y, df['计算总资产'], df['资产总计(万元)'])

# print(list(m))

df['是否平衡'] = df.apply(lambda r: r['计算总资产'] == r['资产总计(万元)'], axis=1)
# print(df)
print(df['是否平衡'])
df['差额'] = df.apply(lambda r: r['计算总资产'] - r['资产总计(万元)'], axis=1)
# print(df)

# partII Dupont Analysis

# ROE
# 净利润率
# 总资产周转率
# 财务杠杆

di = di.T
di['所有者权益(或股东权益)合计(万元)'] = df['所有者权益(或股东权益)合计(万元)']

di['主营业务收入'] = di.apply(
    lambda r: r['营业利润(万元)'] + r['营业成本(万元)'] + r['营业税金及附加(万元)'] + r['销售费用(万元)'] + r['财务费用(万元)'] + r['管理费用(万元)'] - r[
        '投资收益(万元)'] + r['资产减值损失(万元)'], axis=1)
di['净利润率'] = di.apply(lambda r: r['净利润(万元)'] / r['主营业务收入'], axis=1)

net_income = di['净利润(万元)'].copy()

di['资产总计(万元)'] = df['资产总计(万元)']

at = di['总资产周转率'] = di.apply(lambda r: r['营业收入(万元)'] / r['资产总计(万元)'], axis=1)

di['负债合计(万元)'] = df['负债合计(万元)']

di['资产总计(万元)'] = df['资产总计(万元)']

fl = di['财务杠杆'] = di.apply(lambda r: r['资产总计(万元)'] / r['所有者权益(或股东权益)合计(万元)'], axis=1)

di['ROE'] = di.apply(lambda r: r['财务杠杆'] * r['总资产周转率'] * r['净利润(万元)'], axis=1)


roe = di['ROE']

#plt.figure()
# roe.plot()
# at.plot('bar')
# fl.plot('bar')



# twin parasite


# calculating TTM

# def month(x):
# return pandas.to_datetime(x.index).month


# shift,rolling(window)
nidf = net_income.to_frame()
nishifted = nidf.apply(lambda row: row['净利润(万元)'] if not row.name.endswith('12-31') else 0, axis=1).shift(-1)

di['净利润TTM'] = (nidf['净利润(万元)'] - nishifted).rolling(window=4).sum()
print(di[['净利润TTM', '净利润(万元)']])
di['ROETTM'] = di.apply(lambda r: r['财务杠杆'] * r['总资产周转率'] * r['净利润TTM'], axis=1)


di = di.sort_index()

# di['净利润TTM'].plot()
# di['财务杠杆'].plot()
di['总资产周转率'].plot()
# di['ROETTM'].plot()

plt.show()





