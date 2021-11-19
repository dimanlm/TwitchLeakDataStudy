#!/usr/bin/env python3

import pandas as pd
import numpy as np
import requests

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
    monthlyRevenueColumn = pd.DataFrame(twitchData, columns=['total_monthly_revenue'])
    return (monthlyRevenueColumn.min().values[0])


def streamersMaximumRevenue(twitchData):
    monthlyRevenueColumn = pd.DataFrame(twitchData, columns=['total_monthly_revenue'])
    return (monthlyRevenueColumn.max().values[0])


def streamersAverageRevenue(twitchData):
    monthlyRevenueColumn = pd.DataFrame(twitchData, columns=['total_monthly_revenue'])
    return (round(monthlyRevenueColumn.mean().values[0], 2))


def streamersMedianRevenue(twitchData):
    monthlyRevenueColumn = pd.DataFrame(twitchData, columns=['total_monthly_revenue'])
    return (monthlyRevenueColumn.median().values[0])

"----------------------------------------------------"
"----------------------------------------------------"

CSV_FILE_NAME = '/all_revenues.csv'
PATH_TO_THE_CSV_FILE = 'LeakTwitch/all_revenues/2020/01'
importedTwitchData = pd.read_csv(PATH_TO_THE_CSV_FILE+CSV_FILE_NAME)

streamersMonthlyRevenue = computeStreamersMonthlyIncome(importedTwitchData)    
addNewColumnToDataFrame(importedTwitchData, 'total_monthly_revenue', streamersMonthlyRevenue)
