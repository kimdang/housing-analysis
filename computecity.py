import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#### THIS SCRIPT WILL COMPUTE CITY AS USER REQUEST ####

def plothistory(targetDF):
    plt.plot('dt', 'price', data=targetDF)
    plt.savefig('Example.jpg')
