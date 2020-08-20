import pandas as pd 
import execute
# execute.py handle all MYSQL communication and contains DB login information 


filename = ("ZillowByCity.csv")


data = pd.read_csv(filename)
cityCount = data["RegionName"].count()
entryCount = len(data.columns)-8  
# first 8 columns contain miscellaneous information therefore discard 




print(f"There are {cityCount} cities in dataset. Each city contains {entryCount} entries.")

print("Do you want to populate the index table with this dataset? (y/n) \n")

proceed = input()


RegionName_list = []
for i in range(cityCount):
    text = data['RegionName'][i]
    new_text = text.replace("'", "")
    RegionName_list.append(new_text)

data['NewRegionName'] = RegionName_list
# Some names contain single quote that SQL query cannot be processed
# This is work-around


if proceed == "y":
    for i in range(cityCount):
        text = "(%s, '%s', '%s')" %(data['RegionID'][i], data['NewRegionName'][i], data['StateName'][i])
        query = "INSERT INTO myapp_indextable (regionID, regionName, regionState) VALUES %s" %(text)
        execute.run_query(query)

print('Done!')






#####################################################################
####### THIS IS AN ATTEMPT TO IMPORT DATA IN 1 SINGLE QUERY #########
# if proceed == "y":
#     total = ""
#     for i in range(cityCount):
#         if (i != (cityCount-1)):
#             text = "(%s, %s, %s), " %(data['RegionID'][i], data['RegionName'][i], data['StateName'][i])
#         else:
#             text = "(%s, %s, %s) " %(data['RegionID'][i], data['RegionName'][i], data['StateName'][i])
#         total = total + text 
        
        
# insert_query = "INSERT INTO myapp_indextable (regionID, regionName, regionState) VALUES %s" %(total)
# execute.run_query(insert_query)
#####################################################################