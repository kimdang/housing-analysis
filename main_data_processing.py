
from datatools import DataSet
import SQLtools

example = DataSet('TopTierByCity.csv', 'toptier')
example.sanitize(before2000=False)
# example.split()
# example.multi(process_no=5)
# print(example)


SQLtools.tostring(example.indexdf, key='index')