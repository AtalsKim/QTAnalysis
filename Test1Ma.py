# -*- coding:utf-8 -*-
__author__ = 'Atlas'
'''
Author: Atlas Kim
Description: 连续涨停三次数据筛选
Modification: 
'''

import os
import pandas as pd
import numpy as np
from pandas import DataFrame as df
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号


def main():
    DataDir = r'E:\PT\量化分析\1990.12-2019.2.15沪深股市日线数据\excel'
    xlist = os.listdir(DataDir)
    for xfiles in xlist:
        # 绝对路径
        Abspath = os.path.join(DataDir, xfiles)
        print('P: ', xfiles)
        # 符合要求的Series
        OnePD = loadxls(Abspath)
        if OnePD.empty:
            continue
        else:
            savepath = os.path.join(DataDir, 'Filt_'+xfiles)
            fig = plt.figure()
            ax = plt.subplot(111)
            plt.plot(OnePD['日期'],OnePD['收盘'])
            plt.xticks(rotation=45)
            plt.ylabel('收盘价')
            tname = OnePD['名称'].get_values()[0]
            plt.title(tname)
            fig.savefig(savepath + '.tif', format='tif')
            plt.close()
            OnePD.to_excel(savepath)
            print("Saved to: ",savepath)



# 读取xls 并且识别连续涨停天数
def loadxls(xlspath, percent = 0.1, days = 3):
    Qdf = pd.read_excel(xlspath)
    Qdf['indexval'] = Qdf.index.get_values()
    # 筛选为涨停
    Limit_up = Qdf.loc[(Qdf['涨幅'] >= percent)]
    # 与前一天差值list
    diffone = severaldays(Limit_up, days)
    if diffone.size == 0:
        print("没有数据符合")
        return pd.DataFrame()
    else:
        print("数据符合")
        selectrange = []
        for updays in diffone:
            if updays in selectrange:
                continue
            else:
                selectrange.extend(range(updays-30, updays+30))
        selected_df = Qdf.loc[selectrange]
        return selected_df
    # 由于是日表前后三十行


# 输出序列号,List
def severaldays(df1, days):
    df0 = df1
    for i in range(days):
        x = df1['indexval'].diff()
        dfones = x.loc[x == 1]
        indexval = dfones.index.get_values()
        df1 = df1.ix[indexval]
    return df1.index.get_values()



if __name__ == '__main__':
    main()