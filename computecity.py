import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import base64
from io import BytesIO


def plothistory(targetDF):
    fig = plt.figure(figsize=(10,5))
    ax = fig.add_subplot(111)
    line = plt.plot('dt', 'price', data=targetDF)
    plt.ylabel('Average Home Value')
    plt.grid(b=True, color='k', linestyle='dotted', linewidth='0.5')
    ax.set_yticklabels(['${:,}'.format(int(x)) for x in ax.get_yticks().tolist()])

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    return image_png