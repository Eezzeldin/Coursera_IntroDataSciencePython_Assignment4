import pandas as pd
import numpy as np
import cleaning as c

path      = '/Users/emadezzeldin/Emad Dropbox/Emad Mohamed/Automating_Applying/coursera/advancedpython/4/RawData/'
filename  = 'City_Zhvi_AllHomes.csv'
housesfile= path + filename
houses    = pd.read_csv (housesfile)
def trimdf (houses):
    columns = houses.columns
    numcol  = columns [8:]
    def get2000 (column):
        strcolumn = str (column)
        year      = strcolumn.split('-')[0]
        return int(year) >= 2000 and int(year) <= 2016
    wantedcol= [col for col in numcol if get2000(col)]
    wantedcol = wantedcol + ['RegionID','RegionName'	,'State'	,'Metro'	,'CountyName'	,'SizeRank']
    c.WantedCols (houses,wantedcol)
    return houses
houses    = trimdf(houses)
#print (houses)

def convertoquarters (houses):
    '''
    A quarter is a specific three month period, Q1 is January through March, Q2 is April through June, Q3 is July through September, Q4 is October through December.
    '''
    Quarter = {'-01':'q1','-02':'q1','-03':'q1' , '-04':'q2' , '-05':'q2' , '-06': 'q2' , '-07':'q3' , '-08':'q3' , '-09':'q3' , '-10':'q4' , '-11':'q4' , '-12':'q4'}
    #print (houses.columns[6:])
    #print ('2000-01'.replace ('-01',Quarter['-01']))
    replacement   = [str (col).replace ('-' + str(col).split('-')[1],Quarter ['-'+str(col).split('-')[1]]) for col in houses.columns[6:] ]
    print (replacement)
    original      = houses.columns[6:]

    def getReplacementDictionary(original):
        # return a dictionary of renames
        myreplacementdict = {}
        for i in range(len(original)):
            myreplacementdict [original[i]] = replacement [i]
        return myreplacementdict
    print   (getReplacementDictionary(original))
    myreplacementdict = getReplacementDictionary(original)
    houses.rename(columns = myreplacementdict,inplace=True)
    #print (houses)
    return houses
print (convertoquarters (houses))
