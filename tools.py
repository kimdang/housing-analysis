import pandas as pd 
import datetime

def clean (rawDF, ID, dropcolumn):
    print("Preparing RegionID %s data set." %(ID))
    city = rawDF.loc[rawDF['RegionID'] == ID]
    city = city.T
    city = city.drop(city.index[0:dropcolumn])
    city = city.dropna().astype(int) 
    # Elimate N/A from data set
    count = len(city.index)
    date_list = []

    # For index, convert string --> datetime to make graphing easy
    for i in range(count):
        date = datetime.datetime.strptime(city.index[i], "%Y-%m-%d")
        date_list.append(date)
        new_df = pd.DataFrame(city, index=date_list)

    return new_df