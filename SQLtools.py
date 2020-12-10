
import pandas as pd



def tostring(df, key):

    colname = df.columns.values
    rowcount = df[colname[0]].count()

    if key == 'index':
        total = ""
        for j in range(rowcount):
            if (j != (rowcount-1)):
                segment = "(%s, '%s', '%s'), " %(df[colname[0]][j], df[colname[1]][j], df[colname[2]][j])
            else:
                segment = "(%s, '%s', '%s')" %(df[colname[0]][j], df[colname[1]][j], df[colname[2]][j])
            total = total + segment
    # df DataFrame has 3 columns: regionID, cityname, statename 
    # df DataFrame goes into database to serve as index table 

    return total




