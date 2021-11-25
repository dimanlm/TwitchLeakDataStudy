#!/usr/bin/env python3

import pandas as pd
import numpy as np
import requests
import time
import matplotlib.pyplot as plt

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
    monthlyRevenueOverviewDf = pd.DataFrame(twitchData, columns=[USER_ID_COLUMN,TOTAL_MONTHLY_REVENUE_COLUMN])
    getMinIncomeThisMonth = monthlyRevenueOverviewDf.loc[monthlyRevenueOverviewDf[TOTAL_MONTHLY_REVENUE_COLUMN].idxmin()]
    return (getMinIncomeThisMonth)


def streamersMaximumRevenue(twitchData):
    monthlyRevenueOverviewDf = pd.DataFrame(twitchData, columns=[USER_ID_COLUMN,TOTAL_MONTHLY_REVENUE_COLUMN])
    getMaxIncomeThisMonth = monthlyRevenueOverviewDf.loc[monthlyRevenueOverviewDf[TOTAL_MONTHLY_REVENUE_COLUMN].idxmax()]
    return (getMaxIncomeThisMonth)


def streamersAverageRevenue(twitchData):
    monthlyRevenueColumn = pd.DataFrame(twitchData, columns=[TOTAL_MONTHLY_REVENUE_COLUMN])
    return (round(monthlyRevenueColumn.mean().values[0], 2))


def streamersMedianRevenue(twitchData):
    monthlyRevenueColumn = pd.DataFrame(twitchData, columns=[TOTAL_MONTHLY_REVENUE_COLUMN])
    return (monthlyRevenueColumn.median().values[0])

"----------------------------------------------------"
"----------------------------------------------------"

if __name__ == "__main__":
    t0 = time.time()

    TOTAL_MONTHLY_REVENUE_COLUMN = 'total_monthly_revenue'
    USER_ID_COLUMN = 'user_id'
    TOTAL_MONTHS = 12
    CSV_FILE_NAME = '/all_revenues.csv'

    allMonthlyRevenuesDataf = pd.DataFrame()
    monthlyRevenueOverviewDataf = pd.DataFrame()
    annualRevenueOverviewDf = pd.DataFrame()

    for i in range(1,TOTAL_MONTHS+1):
        if i<10:
            PATH_TO_THE_CSV_FILE = 'LeakTwitch/all_revenues/2020/0'+str(i)
        else:
            PATH_TO_THE_CSV_FILE = 'LeakTwitch/all_revenues/2020/'+str(i)
        
        importedTwitchData = pd.read_csv(PATH_TO_THE_CSV_FILE+CSV_FILE_NAME)
        addNewColumnToDataFrame(importedTwitchData, TOTAL_MONTHLY_REVENUE_COLUMN, computeStreamersMonthlyIncome(importedTwitchData))

        monthlyRevenueOverviewDataf.loc[i, "Minimum"]= streamersMinimumRevenue(importedTwitchData)[TOTAL_MONTHLY_REVENUE_COLUMN]
        monthlyRevenueOverviewDataf.loc[i, "Maximum"]= streamersMaximumRevenue(importedTwitchData)[TOTAL_MONTHLY_REVENUE_COLUMN]
        monthlyRevenueOverviewDataf.loc[i, "Who?"]= getStreamersNickname(str(streamersMaximumRevenue(importedTwitchData)[USER_ID_COLUMN])[:-2])
        monthlyRevenueOverviewDataf.loc[i, "Average"]= streamersAverageRevenue(importedTwitchData)
        monthlyRevenueOverviewDataf.loc[i, "Median"]= streamersMedianRevenue(importedTwitchData)

        selectedColumnsToAppend = importedTwitchData[[USER_ID_COLUMN, TOTAL_MONTHLY_REVENUE_COLUMN]].copy()
        allMonthlyRevenuesDataf=allMonthlyRevenuesDataf.append(selectedColumnsToAppend, ignore_index=True)   

    aggregateRevenues = {TOTAL_MONTHLY_REVENUE_COLUMN: 'sum'}
    eachStreamerTotalRevenueDataf= allMonthlyRevenuesDataf.groupby(USER_ID_COLUMN, as_index=False).aggregate(aggregateRevenues).reindex(columns=allMonthlyRevenuesDataf.columns)

    annualRevenueOverviewDf.loc[i, "annual_Minimum"]= streamersMinimumRevenue(eachStreamerTotalRevenueDataf)[TOTAL_MONTHLY_REVENUE_COLUMN]
    annualRevenueOverviewDf.loc[i, "annual_Maximum"]= streamersMaximumRevenue(eachStreamerTotalRevenueDataf)[TOTAL_MONTHLY_REVENUE_COLUMN]
    annualRevenueOverviewDf.loc[i, "annual_Average"]= streamersAverageRevenue(eachStreamerTotalRevenueDataf)
    annualRevenueOverviewDf.loc[i, "annual_Median"]= streamersMedianRevenue(eachStreamerTotalRevenueDataf)

    highestPaidStreamer = getStreamersNickname(str(streamersMaximumRevenue(eachStreamerTotalRevenueDataf).values[0])[:-2])
 
    print(monthlyRevenueOverviewDataf)
    print('\n')
    print(annualRevenueOverviewDf)
    print("Highest paid streamer of 2020: " + highestPaidStreamer)

    print("\nData scanned in ", round(time.time()-t0, 2), " seconds\n")