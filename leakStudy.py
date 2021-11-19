#!/usr/bin/env python3

import pandas as pd
import numpy as np
import requests
import time

"----------------------------------------------------"

def addNewColumnToDataFrame(aDataFrame, newColumnName, newColumnData):
    aDataFrame[newColumnName] = newColumnData


def getStreamersNickname(streamersUserID):
    API_REQUEST_NICKNAME = "https://customapi.aidenwallis.co.uk/api/v1/twitch/toName/"+streamersUserID
    return (requests.get(API_REQUEST_NICKNAME).text)


def computeStreamersMonthlyIncome(twitchData):
    allRevenueColumns = twitchData.columns.str.contains('_gross')
    return(twitchData.iloc[:, allRevenueColumns].sum(axis=1))


def streamersMinimumRevenue(twitchData):
    monthlyRevenueDf = pd.DataFrame(twitchData, columns=[USER_ID_COLUMN,TOTAL_MONTHLY_REVENUE_COLUMN])
    getMinValue = monthlyRevenueDf.loc[monthlyRevenueDf[TOTAL_MONTHLY_REVENUE_COLUMN].idxmin()]
    return (getMinValue)


def streamersMaximumRevenue(twitchData):
    monthlyRevenueDf = pd.DataFrame(twitchData, columns=[USER_ID_COLUMN,TOTAL_MONTHLY_REVENUE_COLUMN])
    getMaxValue = monthlyRevenueDf.loc[monthlyRevenueDf[TOTAL_MONTHLY_REVENUE_COLUMN].idxmax()]
    return (getMaxValue)


def streamersAverageRevenue(twitchData):
    monthlyRevenueColumn = pd.DataFrame(twitchData, columns=[TOTAL_MONTHLY_REVENUE_COLUMN])
    return (round(monthlyRevenueColumn.mean().values[0], 2))


def streamersMedianRevenue(twitchData):
    monthlyRevenueColumn = pd.DataFrame(twitchData, columns=[TOTAL_MONTHLY_REVENUE_COLUMN])
    return (monthlyRevenueColumn.median().values[0])

"----------------------------------------------------"
"----------------------------------------------------"

if __name__ == "__main__":

    TOTAL_MONTHLY_REVENUE_COLUMN = 'total_monthly_revenue'
    USER_ID_COLUMN = 'user_id'
    TOTAL_MONTHS = 12
    CSV_FILE_NAME = '/all_revenues.csv'

    t0 = time.time()

    monthlyRevenueDf = pd.DataFrame()
    
    for i in range(1,TOTAL_MONTHS+1):

        if i<10:
            PATH_TO_THE_CSV_FILE = 'LeakTwitch/all_revenues/2020/0'+str(i)
        else:
            PATH_TO_THE_CSV_FILE = 'LeakTwitch/all_revenues/2020/'+str(i)
        importedTwitchData = pd.read_csv(PATH_TO_THE_CSV_FILE+CSV_FILE_NAME)
        

        streamersMonthlyRevenue = computeStreamersMonthlyIncome(importedTwitchData)    
        addNewColumnToDataFrame(importedTwitchData, TOTAL_MONTHLY_REVENUE_COLUMN, streamersMonthlyRevenue)

        monthlyRevenueDf.loc[i, "Minimum"]= streamersMinimumRevenue(importedTwitchData)[TOTAL_MONTHLY_REVENUE_COLUMN]
        monthlyRevenueDf.loc[i, "Maximum"]= streamersMaximumRevenue(importedTwitchData)[TOTAL_MONTHLY_REVENUE_COLUMN]
        monthlyRevenueDf.loc[i, "Who?"]= getStreamersNickname(str(streamersMaximumRevenue(importedTwitchData)[USER_ID_COLUMN])[:-2])
        monthlyRevenueDf.loc[i, "Average"]= streamersAverageRevenue(importedTwitchData)
        monthlyRevenueDf.loc[i, "Median"]= streamersMedianRevenue(importedTwitchData)
  
    print(monthlyRevenueDf)
    print("\nData scanned in ", round(time.time()-t0, 2), " seconds\n")