from datatools import DataSet
import SQLtools
import execute
import pickle
import multiprocessing



####### FILL OUT THE 2 LISTS BELOW, MAKE SURE ITEMS ARE IN CORRECT ORDER! ########
csvfile = ['TopTierByCity.csv', 'MidTierByCity.csv', 'BottomTierByCity.csv', 'OneBedByCity.csv', 'TwoBedByCity.csv', 'ThreeBedByCity.csv', 'FourBedByCity.csv', 'FiveBedByCity.csv']
csvname = ['toptier', 'midtier', 'bottomtier', 'onebed', 'twobed', 'threebed', 'fourbed', 'fivebed']



def save_obj(obj, name):
    filename = open(name, "wb")
    pickle.dump(obj, filename)
    


def load_obj(name):
    filename = open(name, "rb")
    return(pickle.load(filename))



def insertStateToDB(state, tier, tierDict):
    # used for multi-processing 
    # this function will insert state's data in form dictionary into database (e.g. NY_toptier, CA_onebed, IL_bottomtier)
    createTableQuery = "CREATE TABLE IF NOT EXISTS %s_%s (price INT, date DATETIME NOT NULL, regionid INT, FOREIGN KEY (regionid) REFERENCES main_index(regionid))" %(state, tier)
    execute.run_query(createTableQuery)
    stateText = SQLtools.dftostring(tierDict[state], key='state')
    insertQuery = "INSERT INTO %s_%s (price, date, regionid) VALUES %s" %(state, tier, stateText)
    execute.run_query(insertQuery)
    print("%s_%s is now in MySQL database." %(state, tier))



######################## SCRIPTS TO EXECUTE BEGIN HERE ######################## 



print("Do you want to import the index tables? (yes/no)")
createIndexTable = input()

# This script creates 8 index tables, which are subsequently combined to create 1 main index table via UNION query. See below.
if createIndexTable == "yes":
    for filename, name in zip(csvfile, csvname):
        temp = DataSet(filename, name) 
        temp.clean(before2000=False)
        text = SQLtools.dftostring(temp.indexdf, key='index')
        createQuery = "CREATE TABLE IF NOT EXISTS %s_index (regionid INT PRIMARY KEY, cityname VARCHAR(255), statename VARCHAR(255))" %(name)
        execute.run_query(createQuery)
        insertQuery = "INSERT INTO %s_index (regionid, cityname, statename) VALUES %s" %(name, text)
        execute.run_query(insertQuery)
    print("All index tables have been created in MySQL database. Please go to database and execute appropriate queries. FYI, these queuries can be found in main_data_processing.py")





# # You must execute 2 queries. First is UNION query to combine all index tables to create table main_index: 
# CREATE TABLE main_index AS 
# SELECT * FROM toptier_index 
# UNION 
# SELECT * FROM midtier_index
# UNION 
# SELECT * FROM bottomtier_index
# UNION 
# SELECT * FROM onebed_index 
# UNION 
# SELECT * FROM twobed_index 
# UNION 
# SELECT * FROM threebed_index 
# UNION 
# SELECT * FROM fourbed_index
# UNION 
# SELECT * FROM fivebed_index
# ORDER BY regionid; 
# # Second is ALTER query to mark the primary key in newly createtable table main_index:
# ALTER TABLE main_index
# ADD PRIMARY KEY (regionid);





print("Do you want to process raw data? (yes/no)")
processRawData = input()

# This script saves the each data set, which is to be recalled later. It is done this way to save times because each data set is expected to be loaded multiple times during development. Only need to be executed once!  
if processRawData == 'yes':
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

# This script handle data import. Multi-processing is used and 5 processes are started at once. 
if sendToDatabase == 'yes':    
    print("Each data set must be imported individually. \nSelect from the following: toptier, bottomtier, midtier, onebed, twobed, threebed, fourbed, or fivebed")
    tier = input()
    
    while tier != 'done':    
        try: 
            tempDict = load_obj("%soutput" %(tier))
            statelist = list(tempDict.keys())

            howmanyprocess = 3
            for x in range(0, len(statelist), howmanyprocess):
                composite = statelist[x:x+howmanyprocess]
                print('Working on: ' + ' '.join(composite))
        
                for state in composite:
                    process = multiprocessing.Process(target=insertStateToDB, args=[state, tier, tempDict])
                    process.start()
                process.join() # It is important that this code is located outside the FOR loop! The FOR loop continues on the iteration without delay or waiting for the processes to finish. 
                # process.join() puts a stop or delay which will enable the 5 processes to finish before the FOR loop continues on 
        except LookupError:
            print("Your input is invalid!")
        
        print("What other data set do you want to import? (toptier, bottomtier, midtier, onebed, twobed, threebed, fourbed, fivebed) \nIf done, please enter done.")
        tier = input()
