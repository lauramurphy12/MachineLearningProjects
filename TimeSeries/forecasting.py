import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels as sm
from sklearn.metrics import mean_squared_error, mean_absolute_error
from math import sqrt
from statsmodels.tsa.stattools import adfuller

def select_country(dataset, country_column, date_column, measurement, start_date, country):
    country = dataset.loc[dataset[country_column] == country]
    country = country[[date_column,measurement]]
    country = country[(country[date_column] >= start_date)]
    country = country.set_index(date_column)
    country = country.sort_index()
    return country
	
def train_test_split(series, periods):
    train = series[:len(series)-periods]
    test = series[len(series)-periods:]
    return(train, test)
	
def error_metrics(forecast, test):
    mae = mean_absolute_error(test, forecast)
    mape = np.mean(np.abs(forecast - test)/np.abs(test))
    rmse = sqrt(mean_squared_error(test, forecast))
    print('Mean Absolute Error: %f , Mean Absolute Percentage #Error: %f, Root Mean Squared Error: %f' % (mae, mape, rmse))
    
def downsampling(series, seasonal_period):
    return series.resample(seasonal_period).mean().astype(int)

def test_stationarity(series):
    adfTest = adfuller(series, autolag='AIC')
    print("Results of the Augmented Dickey Fuller Test")
    adf_results = pd.Series(adfTest[0:4], index=['ADF Test statistic', 'p-value', 'Lag', 'Number of Observations'])
    for confidence_level, value in adfTest[4].items():
        adf_results = adf_results.append(pd.Series([value], index=['Critical value cutoff %s' %confidence_level]))
    print(adf_results)
