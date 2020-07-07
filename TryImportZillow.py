import sqlite3
import pandas as pd 

data = pd.read_csv("ZillowByCity.csv")
cityCount = data["RegionName"].count()
entryCount = len(data.columns)-8  # First 8 columns are not home prices.

print(f"There are {cityCount} cities in dataset. Each city has {entryCount} entries.\n")


subdata = data[data.StateName == "CA"]

regionID = subdata['RegionID'].tolist()
regionName = subdata['RegionName'].tolist()
regionState = subdata['StateName'].tolist()



conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()

for i in range(len(regionID)):
    text = "(%s, '%s', '%s')" %(regionID[i], regionName[i], regionState[i])
    query = "INSERT INTO myapp_indexTable (regionID, regionName, regionState) VALUES %s" %(text)
    print(query)
    c.execute(query)




print('Data inserted.')




