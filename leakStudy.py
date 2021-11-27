#!/usr/bin/env python3

import pandas as pd
import requests
import time
from matplotlib import pyplot as plt
from varfile import *

"----------------------------------------------------"

def addNewColumnToDataFrame(aDataFrame, newColumnName, newColumnData):
    aDataFrame[newColumnName] = newColumnData


def getStreamersNickname(streamersUserID):
    API_REQUEST_NICKNAME = "https://customapi.aidenwallis.co.uk/api/v1/twitch/toName/"+streamersUserID
    return (requests.get(API_REQUEST_NICKNAME).text)


def checkInternetConnection():
    connected = True
    try:
	    request = requests.get("http://www.google.com", timeout=5)
    except (requests.ConnectionError, requests.Timeout) as exception:
        connected = False
    return connected


def computeStreamersMonthlyIncome(twitchDataf):
    allRevenueColumns = twitchDataf.columns.str.contains('_gross')
    return(twitchDataf.iloc[:, allRevenueColumns].sum(axis=1))


def streamersMinimumRevenue(twitchDataf):
    monthlyRevenueOverviewDf = pd.DataFrame(twitchDataf, columns=[USER_ID_COLUMN,TOTAL_MONTHLY_REVENUE_COLUMN])
    getMinIncomeThisMonth = monthlyRevenueOverviewDf.loc[monthlyRevenueOverviewDf[TOTAL_MONTHLY_REVENUE_COLUMN].idxmin()]
    return (getMinIncomeThisMonth)


def streamersMaximumRevenue(twitchDataf):
    monthlyRevenueOverviewDf = pd.DataFrame(twitchDataf, columns=[USER_ID_COLUMN,TOTAL_MONTHLY_REVENUE_COLUMN])
    getMaxIncomeThisMonth = monthlyRevenueOverviewDf.loc[monthlyRevenueOverviewDf[TOTAL_MONTHLY_REVENUE_COLUMN].idxmax()]
    return (getMaxIncomeThisMonth)


def streamersAverageRevenue(twitchDataf):
    monthlyRevenueColumn = pd.DataFrame(twitchDataf, columns=[TOTAL_MONTHLY_REVENUE_COLUMN])
    return (round(monthlyRevenueColumn.mean().values[0], 2))


def streamersMedianRevenue(twitchDataf):
    monthlyRevenueColumn = pd.DataFrame(twitchDataf, columns=[TOTAL_MONTHLY_REVENUE_COLUMN])
    return (monthlyRevenueColumn.median().values[0])


def aggregateAllRevenues(twitchDataf, aggFunction):
    return (twitchDataf.groupby(USER_ID_COLUMN, as_index=False).aggregate(aggFunction).reindex(columns=twitchDataf.columns))


def getRevenueOverview(aDataFrame, overviewDataFrame):
    overviewDataFrame.loc[i, "Average"]= streamersAverageRevenue(aDataFrame)
    overviewDataFrame.loc[i, "Median"]= streamersMedianRevenue(aDataFrame)
    overviewDataFrame.loc[i, "Minimum"]= streamersMinimumRevenue(aDataFrame)[TOTAL_MONTHLY_REVENUE_COLUMN]
    overviewDataFrame.loc[i, "Maximum"]= streamersMaximumRevenue(aDataFrame)[TOTAL_MONTHLY_REVENUE_COLUMN]
    if(checkInternetConnection()):
        overviewDataFrame.loc[i, "Who_max?"]= getStreamersNickname(str(streamersMaximumRevenue(aDataFrame)[USER_ID_COLUMN])[:-2])
    else:
        overviewDataFrame.loc[i, "Who_max?"]= str(streamersMaximumRevenue(aDataFrame)[USER_ID_COLUMN])[:-2]  
    return overviewDataFrame


def makePlotsToSeeTheData (monthlyDataFrame, totalRevDataFrame):
    fig, axs = plt.subplots(4, 1, constrained_layout=True)
    fig.suptitle('Twitch data plots', fontsize=16)
    
    plt.xticks(monthlyDataFrame['Median'], monthlyDataFrame.index.values )
    axs[0].plot(monthlyDataFrame['Median'] )
    axs[0].set_title('Monthly median salary variations')
    axs[0].set(xlabel='Months', ylabel='Median (USD)')

    plt.xticks(monthlyDataFrame['Average'], monthlyDataFrame.index.values )
    axs[1].plot(monthlyDataFrame['Average'] )
    axs[1].set_title('Monthly avg salary variations')
    axs[1].set(xlabel='Months', ylabel='Average (USD)')

    plt.xticks(monthlyDataFrame['Maximum'], monthlyDataFrame.index.values )
    axs[2].plot(monthlyDataFrame['Maximum'] )
    axs[2].set_title('Monthly maximum salary variations')
    axs[2].set(xlabel='Months', ylabel='Maximum (USD)')

    axs[3].scatter(TOTAL_MONTHLY_REVENUE_COLUMN, USER_ID_COLUMN, data=totalRevDataFrame)
    axs[3].set_title('Money distribution')
    axs[3].set(xlabel='USD', ylabel='IDs')
    
    plt.show()

"----------------------------------------------------"
"----------------------------------------------------"

if __name__ == "__main__":
    t0 = time.time()

    allMonthlyRevenuesDataf = pd.DataFrame()
    monthlyRevenueOverviewDataf = pd.DataFrame()
    annualRevenueOverviewDataf = pd.DataFrame()

    for i in range(1,TOTAL_MONTHS+1):
        if i<10:
            PATH_TO_THE_CSV_FILE = PATH_TO+'0'+str(i)
        else:
            PATH_TO_THE_CSV_FILE = PATH_TO+str(i)
        
        importedTwitchData = pd.read_csv(PATH_TO_THE_CSV_FILE+CSV_FILE_NAME)
        addNewColumnToDataFrame(importedTwitchData, TOTAL_MONTHLY_REVENUE_COLUMN, computeStreamersMonthlyIncome(importedTwitchData))
        monthlyRevenueOverviewDataf = getRevenueOverview(importedTwitchData, monthlyRevenueOverviewDataf)
        selectedColumnsToAppend = importedTwitchData[[USER_ID_COLUMN, TOTAL_MONTHLY_REVENUE_COLUMN]].copy()
        allMonthlyRevenuesDataf=allMonthlyRevenuesDataf.append(selectedColumnsToAppend, ignore_index=True)   

    aggregateRevenuesFun = {TOTAL_MONTHLY_REVENUE_COLUMN: 'sum'}
    eachStreamerTotalRevenueDataf= aggregateAllRevenues(allMonthlyRevenuesDataf, aggregateRevenuesFun)
    annualRevenueOverviewDataf = getRevenueOverview(eachStreamerTotalRevenueDataf, annualRevenueOverviewDataf)
    
    if(checkInternetConnection()):
        highestPaidStreamer = getStreamersNickname(str(streamersMaximumRevenue(eachStreamerTotalRevenueDataf).values[0])[:-2])
    else:
        highestPaidStreamer = str(streamersMaximumRevenue(eachStreamerTotalRevenueDataf).values[0])[:-2]

    print(monthlyRevenueOverviewDataf)
    print('\n')
    print(annualRevenueOverviewDataf)
    print("\nThe highest paid streamer of 2020: " + highestPaidStreamer)

    print("\nData scanned in ", round(time.time()-t0, 2), " seconds\n")

    makePlotsToSeeTheData(monthlyRevenueOverviewDataf, eachStreamerTotalRevenueDataf)