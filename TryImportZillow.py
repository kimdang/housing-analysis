import pandas as pd 
import execute

file = ("ZillowByCity.csv")

data = pd.read_csv(file)
cityCount = data["RegionName"].count()
entryCount = len(data.columns)-8  # First 8 columns are not home prices.

print(f"There are {cityCount} cities in dataset. Each city has {entryCount} entries.\n")


subdata = data[data.StateName == "CA"]

regionID = subdata['RegionID'].tolist()
regionName = subdata['RegionName'].tolist()
regionState = subdata['StateName'].tolist()



"""
INSERT DATA INTO myapp_indextable TABLE 
"""
for i in range(len(regionID)):
    text = "(%s, '%s', '%s')" %(regionID[i], regionName[i], regionState[i])
    query = "INSERT INTO myapp_indextable (regionID, regionName, regionState) VALUES %s" %(text)
    execute.run_query(query)

print('Data insertion completed.')




