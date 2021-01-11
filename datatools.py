
import pandas as pd
import numpy as np
import datetime
import multiprocessing




class DataSet: 
    '''
    Class used for processing each data set. Raw data is imported from csv file, splitted into DataFrames by state (e.g. all regions in California is grouped into a DataFrame), processed and stored in a dictionary. Execute in this order: 
    1. clean()
    2. split()
    3. multi_process()

    multi_process() uses multiprocessing to "flatten" each state's DataFrame
    '''

    def __init__(self, csvfile, dataname):

        self.rawData = pd.read_csv(csvfile) 
        # not to be modified!

        self.preprocessData = self.rawData.copy()

        self.indexdf = pd.DataFrame({'regionid': self.preprocessData['RegionID'], 'cityname': self.preprocessData['RegionName'], 'statename': self.preprocessData['StateName']})
        # indexdf serves as reference and template for index table in SQL DB
        
        self.dataname = dataname 

        self.statelist = self.preprocessData['StateName'].unique()

        self.splitted = False

        self.processed = False



    def clean (self, before2000=True):
        '''
        Perform necessary data manipulation to obtain a "clean" DataFrame:
        1. drop irrelevant columns 
        2. drop data before year 2000 if desired 
        3. obtain a list of dates in datetime format to convert DataFrame from str to datetime
        4. remove single quote from city name  
        '''

        dropcols = ['SizeRank', 'RegionName', 'RegionType', 'StateName', 'State', 'Metro', 'CountyName']
        try:
            self.preprocessData.drop(columns=dropcols, inplace=True)
        except LookupError:
            print("DataFrame does not have a specific column.")
        self.preprocessData.set_index('RegionID', inplace=True)
        # these columns need to be removed so that each row can be transposed into its own data set 
   
             
        droprows = list(np.arange(0,48))    
        if not before2000:
            self.preprocessData.drop(self.preprocessData.columns[droprows], axis=1, inplace=True)
        # Zillow raw data covers from 1996 - present, before200=False means data before year 2000 is removed 

        
        datestring = list(self.preprocessData.columns)
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
                return repr(self.processedData)
            else:
                return repr(self.splittedData)
        else:
            return repr(self.preprocessData)
    


    def split(self):

        self.splittedData = {}
        indexdftemp = self.indexdf.copy()
        indexdftemp.set_index('regionid', inplace=True)
        # indexdftemp is necessary because of self.preprocessData.loc[__regionid__]
        # cannot use self.indexdf because it cannot have regionid column as index column (for the purpose of creating index_table in SQL)

        for state in self.statelist:
            # indices_of_state = self.preprocessData.index[indexdftemp['statename']==state].tolist()
            # print("RegionID in " + state + " : " )
            # print(indices_of_state) # for debugging purpose only; please comment out when otherwise
            tempdf = self.preprocessData.loc[indexdftemp['statename']==state]
            self.splittedData.update({state: tempdf})
        # split large df into mulitple dfs by state and place into a dictionary  

        self.splitted = True



    def transpose(self, queue, queueState, state):
        '''
        To be called by multi_processing()
        '''

        statedf = self.splittedData[state]
        transposeDF = pd.DataFrame()
        # transposeDF will contain all transposed region data 

        for index, row in statedf.iterrows():
            tempdf = row.to_frame(name=self.dataname) # convert Series to DataFrame
            regionidarray = np.full(len(tempdf), index) # populate array with only 1 value (regionID)
            tempdf.reset_index(inplace=True)
            tempdf.drop(columns=['index'], inplace=True)
            tempdf['date'] = self.datetimelist
            tempdf['regionid'] = regionidarray 
            tempdf.dropna(inplace=True) # drop row if contain NaN, database won't accept NaN
            transposeDF = transposeDF.append(tempdf, ignore_index=True) # append() return a new DataFrame only 

        queue.put(transposeDF)
        queueState.put(state)
        print(state + " is done.")



    def multi_process(self, process_no):        
        
        rets = []
        # rets contain ALL temporary returned (or transposed) DataFrame
        staterets = []
        # staterets contain the order of returned DataFrame

        for s in range(0, len(self.statelist), process_no):
            composite = list(self.statelist[s:s+process_no])
            print(' '.join(composite) + " are processed at the same time.")
            
            q = multiprocessing.Queue()
            qstate = multiprocessing.Queue()
            processes = []

            for state in composite:
                p = multiprocessing.Process(target=self.transpose, args=(q, qstate, state))
                processes.append(p)
                p.start()
                print("Working on " + state)

            for p in processes:
                ret = q.get()
                rets.append(ret)
                stateret = qstate.get()
                staterets.append(stateret)

            for p in processes:
                p.join()

        self.processedData = dict(zip(staterets, rets))

        self.processed = True

        

            
             