import pandas as pd
import matplotlib.pyplot as plt
from fbprophet import Prophet

import base64
from io import BytesIO


def plothistory(targetDF):
    fig = plt.figure(figsize=(8,4))
    ax = fig.add_subplot(111)
    line = plt.plot('dt', 'price', data=targetDF)
    plt.title("Average Home Value")
    plt.grid(b=True, color='k', linestyle='dotted', linewidth='0.5')
    ax.set_yticklabels(['${:,}'.format(int(x)) for x in ax.get_yticks().tolist()]) # put dollar sign on y-axis values 

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    return image_png




def plotforecast(targetDF):
    df = targetDF[['dt', 'price']]
    df.columns = ['ds', 'y'] # must use appropriate column names

    m = Prophet()
    m.fit(df)
    future = m.make_future_dataframe(periods=60, freq='M') # make a column containing dates for which a prediction is to be made, in this case, 10 years
    forecast = m.predict(future)

    startdt = '2020-01-31' # plot starting from this date 
    startdt_ind = forecast.index[(forecast['ds']== startdt).idxmax()]
    forecastplotdf = forecast[startdt_ind:]
    endprice = int(forecastplotdf['yhat'].values[-1]) # price at the end of forecasted time
    error = [forecastplotdf['yhat_lower'], forecastplotdf['yhat_upper']] # upper and lower error


    fig = plt.figure(figsize=(8,4))
    ax = fig.add_subplot(111)
    ax.errorbar('ds', 'yhat', yerr=error, fmt='8', data=forecastplotdf, color='g')
    plt.title("Forecasted Average Home Value over Next 5 Years")
    plt.grid(b=True, color='k', linestyle='dotted', linewidth='0.5')
    ax.set_yticklabels(['${:,}'.format(int(x)) for x in ax.get_yticks().tolist()])

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    return image_png, endprice

    