from datatools import DataSet
import SQLtools
import execute
import pickle



######## FILL OUT THE 2 LISTS BELOW, MAKE SURE ITEMS ARE IN CORRECT ORDER ########
csvfile = ['TopTierByCity.csv', 'MidTierByCity.csv', 'BottomTierByCity.csv', 'OneBedByCity.csv', 'TwoBedByCity.csv', 'ThreeBedByCity.csv', 'FourBedByCity.csv', 'FiveBedByCity.csv']
csvname = ['toptier', 'midtier', 'bottomtier', 'onebed', 'twobed', 'threebed', 'fourbed', 'fivebed']



def save_obj(obj, name):
    filename = open(name, "wb")
    pickle.dump(obj, filename)
    

def load_obj(name):
    filename = open(name, "rb")
    return(pickle.load(filename))




######## PROCESS DATA FROM CSV FILE AND SAVE ########
# # This code only need to be executed once. Don't forget to comment out once executed.
# for filename, name in zip(csvfile, csvname):
#     print("working on " + name + "...")
#     tempobj = DataSet(filename, name)
#     tempobj.clean(before2000=False)
#     tempobj.split()
#     tempobj.multi_process(process_no=5)
#     save_obj(tempobj.processedData, "%soutput" %(name))
#     print(name + " data has been processed and saved successfully.")








# save_obj(example.processedData, 'toptieroutput')




# savedfile = load_obj("toptieroutput")




# for state in savedfile:
#     createTableQuery = "CREATE TABLE IF NOT EXISTS %s_toptier (price INT, date DATETIME NOT NULL, regionid INT, FOREIGN KEY (regionid) REFERENCES index_table(regionid))" %(state)
#     execute.run_query(createTableQuery)
#     stateText = SQLtools.dftostring(savedfile[state], key='state')
#     insertQuery = "INSERT INTO %s_toptier (price, date, regionid) VALUES %s" %(state, stateText)
#     execute.run_query(insertQuery)
#     print("%s is finished" %(state))


# CREATE INDEX TABLE
# # text = SQLtools.dftostring(example.indexdf, key='index')


# # tablequery = "CREATE TABLE IF NOT EXISTS index_table (regionid INT PRIMARY KEY, cityname VARCHAR(255), statename VARCHAR(255))"
# # execute.run_query(tablequery)

# # insertquery = "INSERT INTO index_table (regionid, cityname, statename) VALUES %s" %(text)
# # execute.run_query(insertquery)

