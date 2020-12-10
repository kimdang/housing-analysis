
from datatools import DataSet
import SQLtools
import execute

example = DataSet('TopTierByCity.csv', 'toptier')
example.sanitize(before2000=False)
example.split()
example.multi(process_no=5)
print(example)
example.dfprocessed.to_pickle("toptiertemp.pkl")

'''
CREATE INDEX TABLE
# text = SQLtools.tostring(example.indexdf, key='index')


# tablequery = "CREATE TABLE IF NOT EXISTS index_table (regionid INT PRIMARY KEY, cityname VARCHAR(255), statename VARCHAR(255))"
# execute.run_query(tablequery)

# insertquery = "INSERT INTO index_table (regionid, cityname, statename) VALUES %s" %(text)
# execute.run_query(insertquery)

'''