#!/usr/bin/env python3

import pandas as pd
import numpy as np

"----------------------------------------------------"

#CSV_FILE_NAME = 'all_revenues.csv'
PATH_TO_THE_CSV_FILE = 'LeakTwitch/all_revenues/2020/01/all_revenues.csv'
importedTwitchData = pd.read_csv(PATH_TO_THE_CSV_FILE)

"----------------------------------------------------"

def addNewColumnToDataFrame(aDataFrame, newColumnName, newColumnData):
    aDataFrame[newColumnName] = newColumnData


def computeStreamersMonthlyIncome(twitchData):
    allRevenueColumns = twitchData.columns.str.contains('_gross')
    return(twitchData.iloc[:, allRevenueColumns].sum(axis=1))


def streamerMinimumRevenue(twitchData):
    monthlyRevenueColumn = pd.DataFrame(twitchData, columns=['total_monthly_revenue'])
    return (monthlyRevenueColumn.min())


def streamerMaximumRevenue(twitchData):
    monthlyRevenueColumn = pd.DataFrame(twitchData, columns=['total_monthly_revenue'])
    return (monthlyRevenueColumn.max())


def streamerAverageRevenue(twitchData):
    monthlyRevenueColumn = pd.DataFrame(twitchData, columns=['total_monthly_revenue'])
    return (monthlyRevenueColumn.mean())


def streamerMedianRevenue(twitchData):
    monthlyRevenueColumn = pd.DataFrame(twitchData, columns=['total_monthly_revenue'])
    return (monthlyRevenueColumn.median())

"----------------------------------------------------"

streamersMonthlyRevenue = computeStreamersMonthlyIncome(importedTwitchData)    
addNewColumnToDataFrame(importedTwitchData, 'total_monthly_revenue', streamersMonthlyRevenue)
