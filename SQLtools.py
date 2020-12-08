
import pandas as pd

def tostring(df, key):
    colname = df.columns.values
    rowcount = df[colname[0]].count()
    if key == 'index':
        total = ""
        for i in range(rowcount):
            text = "(%s, '%s', '%s')" %(df[colname[0]][i], df[colname[1]][i], df[colname[2]][i])
            total = total + text
        print(total)


