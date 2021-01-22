import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objs as go
import statsmodels as sm
from statsmodels.graphics.tsaplots import plot_pacf
from statsmodels.graphics.tsaplots import plot_acf

import warnings
warnings.filterwarnings("ignore")

def acf_pacf_plots(series):
    # Original Time-Series
    fig, axes = plt.subplots(4, 3, figsize=(25,20))
    axes[0, 0].plot(series)
    axes[0, 0].set_title('Raw Data')
    plot_acf(series, ax=axes[0, 1])
    plot_pacf(series, ax=axes[0, 2])

    # 1st Differencing Applied to remove trend
    first_Dif = series.diff(1)
    axes[1, 0].plot(first_Dif[1:])
    axes[1, 0].set_title('1st Order Differencing')
    plot_acf(first_Dif[1:], ax=axes[1, 1])
    plot_pacf(first_Dif[1:], ax=axes[1, 2])

    # Log First Difference to remove variance in the data
    first_Log_Dif = np.log(series).diff(1)
    axes[2, 0].plot(first_Log_Dif[1:])
    axes[2, 0].set_title('Log First Differencing')
    plot_acf(first_Log_Dif[1:], ax=axes[2, 1])
    plot_pacf(first_Log_Dif[1:], ax=axes[2, 2])

    # Seasonal Differencing Applied After 1st Differencing to remove suspected seasonality
    seasonal_Dif = first_Dif.diff(7)
    axes[3, 0].plot(seasonal_Dif[8:])
    axes[3, 0].set_title('Seasonal Differencing After 1st Differencing')
    plot_acf(seasonal_Dif[8:], ax=axes[3, 1])
    plot_pacf(seasonal_Dif[8:], ax=axes[3, 2])


# plots the training set, test set, and the forecasted values for a given time series	
def forecast_whole_plot(train, test, forecast, title, xaxis_title, yaxis_title):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=train.index, y= train.values,
                        mode='lines+markers',
                        name='Training Set'))
    fig.add_trace(go.Scatter(x=test.index, y= test.values,
                        mode='lines+markers',
                        name='Test Set'))
    fig.add_trace(go.Scatter(x=forecast.index, y= forecast.values,
                        mode='lines+markers',
                        name='Forecast'))
    fig.update_layout(title= title,
                       xaxis_title= xaxis_title,
                       yaxis_title= yaxis_title)
    fig.show()

# plot of actual values and values model predicted	
def closeup_forecast_plot(test, forecast, plot_title, xaxis_title, yaxis_title):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=test.index, y= test.values,
                        mode='lines+markers',
                        name='Actual'))
    fig.add_trace(go.Scatter(x=forecast.index, y= forecast.values,
                        mode='lines+markers',
                        name='Forecast'))
    fig.update_layout(title= plot_title,
                       xaxis_title= xaxis_title,
                       yaxis_title= yaxis_title)
    fig.show()


	
	