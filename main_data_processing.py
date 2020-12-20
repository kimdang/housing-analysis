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



print("Do you need to create index table? (yes/no)")
createIndexTable = input()

print("Do you need to process all raw data? (yes/no)")
processRawData = input()


if createIndexTable == "yes":
    midtier = DataSet('MidTierByCity.csv', 'midtier') # use midtier's index DataFrame to create SQL index_table
    midtier.clean(before2000=False)
    text = SQLtools.dftostring(midtier.indexdf, key='index')
    createQuery = "CREATE TABLE IF NOT EXISTS index_table (regionid INT PRIMARY KEY, cityname VARCHAR(255), statename VARCHAR(255))"
    execute.run_query(createQuery)
    insertQuery = "INSERT INTO index_table (regionid, cityname, statename) VALUES %s" %(text)
    execute.run_query(insertQuery)
    print('index_table is created in SQL database.')
    

if processRawData == 'yes':
# This code only need to be executed once.
    for filename, name in zip(csvfile, csvname):
        print("working on " + name + "...")
        tempobj = DataSet(filename, name)
        tempobj.clean(before2000=False)
        tempobj.split()
        tempobj.multi_process(process_no=5)
        save_obj(tempobj.processedData, "%soutput" %(name))
        print(name + " data has been processed and saved successfully.")








# for state in savedfile:
#     createTableQuery = "CREATE TABLE IF NOT EXISTS %s_toptier (price INT, date DATETIME NOT NULL, regionid INT, FOREIGN KEY (regionid) REFERENCES index_table(regionid))" %(state)
#     execute.run_query(createTableQuery)
#     stateText = SQLtools.dftostring(savedfile[state], key='state')
#     insertQuery = "INSERT INTO %s_toptier (price, date, regionid) VALUES %s" %(state, stateText)
#     execute.run_query(insertQuery)
#     print("%s is finished" %(state))


