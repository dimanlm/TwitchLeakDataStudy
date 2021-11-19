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
