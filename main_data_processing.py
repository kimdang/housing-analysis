
from datatools import DataSet
import SQLtools
import execute
import pickle

# example = DataSet('TopTierByCity.csv', 'toptier')
# example.sanitize(before2000=False)
# example.split()
# example.multi(process_no=5)
# print(example)

# def save_obj(obj, name):
#     filename = open(name, "wb")
#     pickle.dump(obj, filename)
    
# save_obj(example.dfprocessed, 'toptieroutput')


def load_obj(name):
    filename = open(name, "rb")
    return(pickle.load(filename))

savedfile = load_obj("toptieroutput")
print(savedfile)




for state in savedfile:
    tablequery = "CREATE TABLE IF NOT EXISTS %s_toptier (price INT, date DATETIME NOT NULL, regionid INT, FOREIGN KEY (regionid) REFERENCES index_table(regionid))" %(state)
    execute.run_query(tablequery)
    print("%s is finished" %(state))


'''
CREATE INDEX TABLE
# text = SQLtools.tostring(example.indexdf, key='index')


# tablequery = "CREATE TABLE IF NOT EXISTS index_table (regionid INT PRIMARY KEY, cityname VARCHAR(255), statename VARCHAR(255))"
# execute.run_query(tablequery)

# insertquery = "INSERT INTO index_table (regionid, cityname, statename) VALUES %s" %(text)
# execute.run_query(insertquery)

'''