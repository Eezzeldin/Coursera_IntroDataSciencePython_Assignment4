import pandas as pd
import numpy as np
import cleaning as c

path      = '/Users/emadezzeldin/Emad Dropbox/Emad Mohamed/Automating_Applying/coursera/advancedpython/4/RawData/'
filename  = 'City_Zhvi_AllHomes.csv'
housesfile= path + filename
houses    = pd.read_csv (housesfile)
#print (houses)
columns = houses.columns
numcol  = columns [8:]
#print (numcol)
def get2000 (column):
    strcolumn = str (column)
    year      = strcolumn.split('-')[0]
    return int(year) >= 2000 and int(year) <= 2016
wantedcol= [col for col in numcol if get2000(col)]
#print (wantedcol)
#wantedcol.append ('State')
#wantedcol.append ('RegionName')
wantedcol = wantedcol + ['RegionID','RegionName'	,'State'	,'Metro'	,'CountyName'	,'SizeRank']
c.WantedCols (houses,wantedcol)
print (houses)
