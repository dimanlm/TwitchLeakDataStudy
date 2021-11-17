#!/usr/bin/env python3

import pandas as pd
import numpy as np


importedTwitchData = pd.read_csv('LeakTwitch/all_revenues/2020/01/all_revenues.csv')

def computeStreamersMonthlyIncome(twitchData):
    allRevenueColumns = twitchData.columns.str.contains('_gross')
    return(twitchData.iloc[:, allRevenueColumns].sum(axis=1))

streamersMonthlyRevenue = computeStreamersMonthlyIncome(importedTwitchData)    
print(streamersMonthlyRevenue)

