import pandas as pd 
import datetime
import execute

def clean (rawDF, ID, dropcolumn):
    # USE FOR ISOLATING AND PREPARING TARGET DATA FOR DATABASE IMPORTATION ONLY
    print("Preparing RegionID %s data set." %(ID))
    city = rawDF.loc[rawDF['RegionID'] == ID]
    city = city.T
    city = city.drop(city.index[0:dropcolumn])
    city = city.dropna().astype(int) 
    # Elimate N/A from data set
    count = len(city.index)
    date_list = []
    # Index: convert to datetime to make graphing easier
    for i in range(count):
        date = datetime.datetime.strptime(city.index[i], "%Y-%m-%d")
        date_list.append(date)
        new_df = pd.DataFrame(city, index=date_list)
    return new_df


def getdatafromDB(regionID):
    getdataquery = "SELECT * FROM city_%s" %(regionID)
    target = execute.run_query(getdataquery, fetch=True, fetch_option='fetchall')
    targetDF = pd.DataFrame(target)
    return targetDF

def capitalize_words(title):
    # Use for capitalization of state name
    title = ' '.join(word[0].upper() + word[1:] for word in title.split(' '))
    return title
