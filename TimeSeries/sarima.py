import itertools
from statsmodels.tsa.statespace.sarimax import SARIMAX
import pandas as pd
import forecasting
import warnings
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error
from math import sqrt

def sarima_model(train, test, trend_order, seasonal_order, forecast_period):
	model = SARIMAX(train, order=trend_order, seasonal_order=seasonal_order)
	model_fit = model.fit()
	yhat = model_fit.forecast(forecast_period)
	return yhat, model_fit.summary()
	

# Walk Forward Validation with expanding window approach. Model is fit with training data with initial starting size. Test set is the next time step in the sequence. A one-step forecast is made.  
# In each iteration the test value of the previous iteration is added to the training set. 
def sarimaWalkForwardVal(series, window_size, trend_order, seasonal_order, forecast_period):
	forecasted_values = list()
	seriesLen = len(series)
	for i in range(window_size, seriesLen):
		# Split data into train and test. 
		train, test = series[0:i],series[i:i+1]
		# fit sarima model with current SARIMA configuration and forecast 1 time step ahead
		yhat, model = sarima_model(train, test, trend_order, seasonal_order, forecast_period)
		forecasted_values.append(yhat[0])	
	test = series[window_size:seriesLen]
	mape = np.mean(np.abs(forecasted_values - test)/np.abs(test))
	rmse = sqrt(mean_squared_error(test, forecasted_values))
	return forecasted_values, mape, rmse


