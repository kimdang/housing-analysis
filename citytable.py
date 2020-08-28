import pandas as pd
import execute
import tools 
import matplotlib.pyplot as plt 
import multiprocessing


filename = ("ZillowByCity.csv")

data = pd.read_csv(filename)
citycount = data['RegionID'].count()


RegionID = data['RegionID']



def insertion (ID):
    ### THIS SECTION CREATES TABLE THAT CORRESPOND TO REGION ID ###
    city_to_db = tools.clean(data, ID, 8)
    dropquery = "DROP TABLE IF EXISTS city_%s" %(ID)
    tablequery = "CREATE TABLE IF NOT EXISTS city_%s (id INT AUTO_INCREMENT PRIMARY KEY, dt DATETIME NOT NULL, price INT)" %(ID)
    execute.run_query(dropquery)
    execute.run_query(tablequery)
    city_to_db.columns = ['price'] # Change column name into "price"


    ### THIS SECTION INSERT DATA INTO EACH TABLE ###
    rowcount = len(city_to_db.index)
    total = ""
    for j in range(rowcount):
        if (j != (rowcount-1)):
                entry = "('%s',%s)," %(city_to_db.index[j], city_to_db['price'][j])
        else:
                entry = "('%s',%s)" %(city_to_db.index[j], city_to_db['price'][j])
        total = total + entry
    
    insertquery = "INSERT INTO city_%s (dt, price) VALUES %s" %(ID, total)
    execute.run_query(insertquery)



    print("Table %s is finished!" %(ID))




##### MULTI-PROCESSING ##### 
for x in range(0, len(RegionID), 20):
    composite = RegionID[x:x+20]
    # 20 processes run at once

    print(composite)
    for ID in composite:
        process = multiprocessing.Process(target=insertion, args=[ID])
        process.start()

    
