# -*- coding: UTF-8 -*-
import numpy as np
import pandas as pd
import tushare as ts
import matplotlib.pyplot as plt
from testdd import *
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['SimHei']
m_f = __file__
# CPI = ts.get_cpi().sort_values('month')
# CPI['cpi'] = CPI['cpi']-100.0
# CPI.to_csv(GetCurPath(m_f)+'/cpi.csv')
#
# df = pd.read_csv(GetCurPath(m_f)+'/cpi.csv')



# plt.figure(figsize=(12,6))
# plt.plot(df['month'],df['cpi'],linewidth=1.2)
# plt.axis('tight')
# plt.xlabel('years',size=12)
# plt.ylabel('%',size=15)
# plt.title('CPI-month-rate',size=12)
#
# plt.show()

# money_supply = ts.get_money_supply().sort_values('month').iloc[228:,:]
#
# money_supply.to_csv(GetCurPath(m_f)+'/MoneySupply.csv')
#
# money_supply.head()
# date = pd.date_range('1997-1-1',periods=len(money_supply),freq='M')
# df = pd.read_csv(GetCurPath(m_f)+'/MoneySupply.csv')
# df.index = date
# df = df.iloc[:,2:8]
# df.rename(columns={'m2_yoy':'m2-increase','m1_yoy':'m1-increase',
#                    'm0_yoy':'m0-increase'},inplace=True)
# df.head()
# print(df)
# df[['m2-increase','m1-increase']].plot(figsize=(12,6))
# plt.xlabel('Date',size=15)
# plt.ylabel('%',size=15)
# plt.title('M2&M1month-increase-same-rate%',size=16)
# plt.annotate('asia-Finance-crisis',size=13,xy=('1997-7-1',24),
#              xytext=('1998-1-1',27),arrowprops=dict(facecolor='black',shrink=0.05),)
# plt.grid(True)
# plt.show(     )

mve= ts.realtime_boxoffice().sort_values('sumBoxOffice')
mve.to_csv(GetCurPath(m_f)+'/box.csv')

print(mve)