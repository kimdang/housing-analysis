
import pandas as pd
import numpy as np
import datetime
import multiprocessing




class DataSet: 
    '''
    Class used for processing each data set. Raw data is imported from csv file, splitted into DataFrames by state (e.g. all regions in California is grouped into a DataFrame), processed and stored in a dictionary. Perform functions in this order: 
    1. sanitized()
    2. split()
    3. multi()

    multi() uses multiprocessing to "flatten" each state's DataFrame
    '''

    def __init__(self, csvfile, dataname):

        self.rawdf = pd.read_csv(csvfile) 
        # not to be modified!

        self.df = self.rawdf.copy()

        self.indexdf = pd.DataFrame({'regionid': self.df['RegionID'], 'cityname': self.df['RegionName'], 'statename': self.df['StateName']})
        # indexdf serves as reference and template for index table in SQL DB
        
        self.dataname = dataname 

        self.statelist = self.df['StateName'].unique()

        self.splitted = False

        self.processed = False



    def sanitize (self, before2000=True):

        dropcols = ['SizeRank', 'RegionName', 'RegionType', 'StateName', 'State', 'Metro', 'CountyName']
        try:
            self.df.drop(columns=dropcols, inplace=True)
        except LookupError:
            print("DataFrame does not have a specific column.")
        self.df.set_index('RegionID', inplace=True)
        # these columns need to be removed so that each row can be transposed into its own data set 
   
             
        droprows = list(np.arange(0,48))    
        if not before2000:
            self.df.drop(self.df.columns[droprows], axis=1, inplace=True)
        # Zillow raw data covers from 1996 - present, before200=False means data before year 2000 is removed 

        
        datestring = list(self.df.columns)
        self.datetimelist = [datetime.datetime.strptime(date, "%Y-%m-%d") for date in datestring]
        # date column will have datetime format instead string by substituting this self.datetimelist
        # can only be executed after certain columns and rows are removed from df 

        newnamelist = []
        for name in self.indexdf['cityname']:
            newname = name.replace("'", "")
            newnamelist.append(newname)
        self.indexdf['cityname'] = newnamelist
        # some city names contain single quote that SQL query cannot be processed
        # remove all single quotes from name 
 


    def __repr__(self):

        if self.splitted:
            if self.processed:
                return repr(self.dfprocessed)
            else:
                return repr(self.dfdict)
        else:
            return repr(self.df)
    


    def split(self):

        self.dfdict = {}

        for state in self.statelist:
            tempdf = self.df.loc[self.indexdf['statename']==state]
            self.dfdict.update({state: tempdf})
        # split large df into mulitple dfs by state and place into a dictionary  

        self.splitted = True



    def transpose(self, queue, state):

        statedf = self.dfdict[state]
        transposeddf = pd.DataFrame()
        # transposeddf contain all transposed region data 

        for index, row in statedf.iterrows():
            tempdf = row.to_frame(name=self.dataname) # convert Series to DataFrame
            regionidarray = np.full(len(tempdf), index) # populate array with only 1 value (regionID)
            tempdf.reset_index(inplace=True)
            tempdf.drop(columns=['index'], inplace=True)
            tempdf['date'] = self.datetimelist
            tempdf['regionid'] = regionidarray 
            transposeddf = transposeddf.append(tempdf, ignore_index=True) # append() return a new DataFrame only 

        queue.put(transposeddf)



    def multi(self, howmany):        
        
        print('This may take a while... ')
        rets = []
        # rets contain temporary returned (or transposed) DataFrame

        for s in range(0, len(self.statelist), process_no):
            composite = list(self.statelist[s:s+process_no])
            
            q = multiprocessing.Queue()
            processes = []

            for state in composite:
                p = multiprocessing.Process(target=self.transpose, args=(q, state))
                processes.append(p)
                p.start()

            for p in processes:
                ret = q.get()
                rets.append(ret)

            for p in processes:
                p.join()

        self.dfprocessed = dict(zip(self.statelist, rets))

        self.processed = True

        

            
             