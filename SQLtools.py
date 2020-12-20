
import pandas as pd



def dftostring(df, key):
    '''
    dftostring() iterates rows of DataFrame and append them onto a string variable
    key argument indicates the purpose of the string variable (e.g. 'index' means the string is used to create index table)
    '''

    colname = df.columns.values
    rowcount = df[colname[0]].count()

    if key == "index":
        totaltext = ""
        for j in range(rowcount):
            if (j != (rowcount-1)):
                text = "(%s, '%s', '%s'), " %(df[colname[0]][j], df[colname[1]][j], df[colname[2]][j])
            else:
                text = "(%s, '%s', '%s')" %(df[colname[0]][j], df[colname[1]][j], df[colname[2]][j])
            totaltext = totaltext + text
    # df has 3 columns: regionID, cityname, statename 
    # df goes into database to serve as index table 

    if key == "state":
        totaltext = ""
        for j in range(rowcount):
            if (j != (rowcount-1)):
                text = "(%s, '%s', %s), " %(df[colname[0]][j], df[colname[1]][j], df[colname[2]][j])
            else:
                text = "(%s, '%s', %s)" %(df[colname[0]][j], df[colname[1]][j], df[colname[2]][j])
            totaltext = totaltext + text
    # df has 3 columns: price, date, regionid

    return totaltext




