import pandas as pd
import numpy as np
import scipy.stats

def WantedCols (df,wantedcol):
    columns = df.columns
    for col in columns:
        if col not in wantedcol:
            del df[col]
    return df
def get_list_of_university_towns():
    '''Returns a DataFrame of towns and the states they are in from the
    university_towns.txt list. The format of the DataFrame should be:
    DataFrame( [ ["Michigan", "Ann Arbor"], ["Michigan", "Yipsilanti"] ],
    columns=["State", "RegionName"]  )

    The following cleaning needs to be done:

    1. For "State", removing characters from "[" to the end.
    2. For "RegionName", when applicable, removing every character from " (" to the end.
    3. Depending on how you read the data, you may need to remove newline character '\n'. '''
    filepath = '/Users/emadezzeldin/Emad Dropbox/Emad Mohamed/Automating_Applying/coursera/advancedpython/4/RawData/'
    filename = 'university_towns.txt'
    myfile   =  filepath + filename
    Universities = pd.read_table (myfile ,header= None)
    #Universities .iloc[0] = 'Universities'
    Universities.rename(columns = {0: 'University'},inplace=True)
    #https://stackoverflow.com/questions/41457322/pandas-rearranging-a-data-frame/41458629#41458629
    #df['model'] = df.col.str.extract('(.*)\[edit\]', expand=False).ffill()
    #df['type'] = df.col.str.extract('([A-Za-z]+)', expand=False)
    #df = df[~df.col.str.contains('\[edit\]')].reset_index(drop=True).drop('col', axis=1)
    #print (df)
    Universities['State'] = Universities.University.str.extract('(.*)\[edit\]', expand=False).ffill()
    #print (Universities)
    Universities['RegionName'] = Universities.University.str.extract('([A-Za-z]+)', expand=False)
    Universities['RegionName'] = Universities.University.str.replace(r'\s+\(.+$', '')
    #print (Universities)
    Universities = Universities[~Universities.University.str.contains('\[edit\]')].reset_index(drop=True).drop('University', axis=1)
    #print_full_rows (Universities)
    #Universities.to_excel('Universities.xlsx')
    return  Universities
def convert_housing_data_to_quarters():
    '''Converts the housing data to quarters and returns it as mean
    values in a dataframe. This dataframe should be a dataframe with
    columns for 2000q1 through 2016q3, and should have a multi-index
    in the shape of ["State","RegionName"].

    Note: Quarters are defined in the assignment description, they are
    not arbitrary three month periods.

    The resulting dataframe should have 67 columns, and 10,730 rows.
    '''
    filepath = '/Users/emadezzeldin/Emad Dropbox/Emad Mohamed/Automating_Applying/coursera/advancedpython/4/RawData/'
    filename = '/City_Zhvi_AllHomes.csv'
    myfile   = filepath + filename
    houses    = pd.read_csv (myfile)

    def trimdf (houses):
        columns = houses.columns
        numcol  = columns [8:]
        def get2000 (column):
            strcolumn = str (column)
            year      = strcolumn.split('-')[0]
            return int(year) >= 2000 and int(year) <= 2016
        wantedcol= [col for col in numcol if get2000(col)]
        wantedcol = wantedcol + ['RegionID','RegionName'	,'State'	,'Metro'	,'CountyName'	,'SizeRank']
        WantedCols (houses,wantedcol)
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
    #print ("=="*20)
    y = (x.set_index (['State','RegionName']).iloc[:,:67])
    #print (y.head())
    #print (y.shape)

    return y
University_Towns = get_list_of_university_towns()
HousingPrices    = convert_housing_data_to_quarters()
HousingPrices_Recession = WantedCols (HousingPrices,['2008q1','2008q2','2008q3','2008q4','2009q1','2009q2'])

df = pd.merge (HousingPrices_Recession.reset_index() , University_Towns , on = University_Towns.columns.tolist(), indicator = '_flag' , how='outer')
group1 = (df [df._flag == 'both'].set_index (['State','RegionName']).iloc [:,:-1])      # a state university
group2 = (df [df._flag ==  'left_only'].set_index (['State','RegionName']).iloc[:,:-1]) # not a state university
print (group1.head())
print ('=='*40)
print (group2.head())

#https://www.coursera.org/learn/python-data-analysis/discussions/weeks/4/threads/F6mWJ7SbEeeKBBKJgknU5g
#hdf['PriceRatio'] = hdf[qrt_bfr_rec_start].div(hdf[rec_bottom])
group1 ['PriceRatio'] = group1['2008q1'] / group1['2009q2']
group2 ['PriceRatio'] = group2['2008q1'] / group2['2009q2']
print (group1.head())
print ('**'*40)
print (group2.head())

x = scipy.stats.ttest_ind (group2['PriceRatio'],group1['PriceRatio'],nan_policy = 'omit')
print (x)
