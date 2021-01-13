import pandas as pd
import matplotlib.pyplot as plt
from fbprophet import Prophet
import os

import base64
from io import BytesIO

class suppress_stdout_stderr(object):
    '''
    A context manager for doing a "deep suppression" of stdout and stderr in
    Python, i.e. will suppress all print, even if the print originates in a
    compiled C/Fortran sub-function.
       This will not suppress raised exceptions, since exceptions are printed
    to stderr just before a script exits, and after the context manager has
    exited (at least, I think that is why it lets exceptions through).

    '''
    def __init__(self):
        # Open a pair of null files
        self.null_fds = [os.open(os.devnull, os.O_RDWR) for x in range(2)]
        # Save the actual stdout (1) and stderr (2) file descriptors.
        self.save_fds = (os.dup(1), os.dup(2))

    def __enter__(self):
        # Assign the null pointers to stdout and stderr.
        os.dup2(self.null_fds[0], 1)
        os.dup2(self.null_fds[1], 2)

    def __exit__(self, *_):
        # Re-assign the real stdout/stderr back to (1) and (2)
        os.dup2(self.save_fds[0], 1)
        os.dup2(self.save_fds[1], 2)
        # Close the null files
        os.close(self.null_fds[0])
        os.close(self.null_fds[1])



def plothistory(targetDF):
    fig = plt.figure(figsize=(8,4))
    ax = fig.add_subplot(111)
    line = plt.plot('date', 'price', data=targetDF)
    plt.title("Average Home Value")
    plt.grid(b=True, color='k', linestyle='dotted', linewidth='0.5')
    ax.set_yticks(ax.get_yticks().tolist()) # REMOVE IN THE FUTURE - PLACED TO AVOID WARNING - IT IS A BUG FROM MATPLOTLIB 3.3.1

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
    # supress error/warning from prophet
    with suppress_stdout_stderr():
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
    ax.set_yticks(ax.get_yticks().tolist()) # REMOVE IN THE FUTURE - PLACED TO AVOID WARNING - IT IS A BUG FROM MATPLOTLIB 3.3.1

    ax.set_yticklabels(['${:,}'.format(int(x)) for x in ax.get_yticks().tolist()])

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    return image_png, endprice
