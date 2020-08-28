import execute
import pandas as pd

#### THIS SCRIPT WILL COMPUTE CITY AS USER REQUEST ####

city = "Sacramento"
state = "CA"




getdataquery = "SELECT * FROM city_%s" %(regionID)

target = execute.run_query(getdataquery, fetch=True, fetch_option='fetchall')

targetDF = pd.DataFrame(target)

print(targetDF)

