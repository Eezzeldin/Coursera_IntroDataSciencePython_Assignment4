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
    #print (replacement)
    original      = houses.columns[6:]

    def getReplacementDictionary(original):
        # return a dictionary of renames
        myreplacementdict = {}
        for i in range(len(original)):
            myreplacementdict [original[i]] = replacement [i]
        return myreplacementdict
    #print   (getReplacementDictionary(original))
    myreplacementdict = getReplacementDictionary(original)
    houses.rename(columns = myreplacementdict,inplace=True)
    #print (houses)
    return houses
#print (convertoquarters (houses))

myhouses   = convertoquarters (houses)
#print (myhouses)

states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}
myhouses.replace ({'State':states},inplace=True)
h  = set([col for col in myhouses.columns [6:]])
#h.remove ('2016q4')
#print (h)
x = (myhouses.loc[:,h].transpose().reset_index().groupby('index').mean().transpose().join(myhouses.iloc [:,0:6]))
#print (x.head())
print ("=="*20)
y = (x.set_index (['State','RegionName']).iloc[:,:67])
