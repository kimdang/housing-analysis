from datatools import DataSet
import SQLtools
import execute
import pickle



######## FILL OUT THE 2 LISTS BELOW, MAKE SURE ITEMS ARE IN CORRECT ORDER! ########
csvfile = ['TopTierByCity.csv', 'MidTierByCity.csv', 'BottomTierByCity.csv', 'OneBedByCity.csv', 'TwoBedByCity.csv', 'ThreeBedByCity.csv', 'FourBedByCity.csv', 'FiveBedByCity.csv']
csvname = ['toptier', 'midtier', 'bottomtier', 'onebed', 'twobed', 'threebed', 'fourbed', 'fivebed']



def save_obj(obj, name):
    filename = open(name, "wb")
    pickle.dump(obj, filename)
    

def load_obj(name):
    filename = open(name, "rb")
    return(pickle.load(filename))



print("Have you created index tables? (yes/no)")
createIndexTable = input()

if createIndexTable == "yes":
    toptier = DataSet('TopTierByCity.csv', 'toptier') # use midtier's index DataFrame to create SQL index_table
    toptier.clean(before2000=False)
    text = SQLtools.dftostring(toptier.indexdf, key='index')
    createQuery = "CREATE TABLE IF NOT EXISTS toptier_index (regionid INT PRIMARY KEY, cityname VARCHAR(255), statename VARCHAR(255))"
    execute.run_query(createQuery)
    insertQuery = "INSERT INTO toptier_index (regionid, cityname, statename) VALUES %s" %(text)
    execute.run_query(insertQuery)
    print('Tables are created in MySQL database.')



print("Do you want to process raw data? (yes/no)")
processRawData = input()

if processRawData == 'yes':
# This script only needs to be executed once.
    for filename, name in zip(csvfile, csvname):
        print("working on " + name + "...")
        tempobj = DataSet(filename, name)
        tempobj.clean(before2000=False)
        tempobj.split()
        tempobj.multi_process(process_no=5)
        save_obj(tempobj.processedData, "%soutput" %(name))
        print(name + " data has been processed and saved successfully.")



print("Do you want to send data to SQL database? (yes/no)")
sendToDatabase = input()

if sendToDatabase == 'yes':    
    for item in csvname:
        nameOfDict = item + "output"
        tempDict = load_obj(nameOfDict)
        for state in tempDict:
            createTableQuery = "CREATE TABLE IF NOT EXISTS %s_%s (price INT, date DATETIME NOT NULL, regionid INT, FOREIGN KEY (regionid) REFERENCES index_table(regionid))" %(state, item)
            execute.run_query(createTableQuery)
            stateText = SQLtools.dftostring(tempDict[state], key='state')
            insertQuery = "INSERT INTO %s_%s (price, date, regionid) VALUES %s" %(state, item, stateText)
            print(insertQuery)
            execute.run_query(insertQuery)
            print("%s_%s is now in MySQL database." %(state, item))


