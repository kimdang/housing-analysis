import sqlite3
import pandas as pd 

data = pd.read_csv("ZillowByCity.csv")
cityCount = data["RegionName"].count()
dateEntry = len(data.columns)-8  # First 8 columns are not home prices.

print(f"There are {cityCount} cities in dataset. Each city has {dateEntry} entries.")

target = "San Diego"

target_index = data.index[data['RegionName']==target]

# subData = data.iloc([8])

print(data.head(5))
# conn = sqlite3.connect('db.sqlite3')
# c = conn.cursor()

# def create_table():
#     c.execute('CREATE TABLE IF NOT EXISTS test_table (value REAL)')


# create_table()
# print('Table created')