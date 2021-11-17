#!/usr/bin/env python3

import pandas as pd
import numpy as np

"----------------------------------------------------"

PATH_TO_THE_CSV_FILE = 'LeakTwitch/all_revenues/2020/01/all_revenues.csv'
importedTwitchData = pd.read_csv(PATH_TO_THE_CSV_FILE)

"----------------------------------------------------"

def addNewColumnToDataFrame(aDataFrame, newColumnName, newColumnData):
    aDataFrame[newColumnName] = newColumnData


def computeStreamersMonthlyIncome(twitchData):
    allRevenueColumns = twitchData.columns.str.contains('_gross')
    return(twitchData.iloc[:, allRevenueColumns].sum(axis=1))

"----------------------------------------------------"

streamersMonthlyRevenue = computeStreamersMonthlyIncome(importedTwitchData)    
addNewColumnToDataFrame(importedTwitchData, 'total_monthly_revenue', streamersMonthlyRevenue)