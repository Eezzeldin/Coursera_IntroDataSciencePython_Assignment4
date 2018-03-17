import pandas as pd
import numpy as np
import re

#===============================================================================
def cleandots(x,mark):
    if str(x) == mark : # The mark was a '.' in HW 3 use case.
        return np.NaN
    else:
        return str (x)
def cleandotsincolumn (series,mark):
    return series.apply (lambda x : cleandots (x,mark))
def cleandotsindataframe (mydataframe,mark):
    columns = mydataframe.columns
    for col in columns:
        mydataframe [col] = cleandotsincolumn (mydataframe [col],mark)
    return mydataframe
#===============================================================================
def rename(df,col,name1 , name2):
    df[col][df[col] == name1] = name2
def WantedCols (df,wantedcol):
    columns = df.columns
    for col in columns:
        if col not in wantedcol:
            del df[col]
    return df
def unWantedCols (df,unwanted):
    for col in unwanted:
        del df [col]
    return df
#===============================================================================
def onlyNum(variable):
    try :
        variable = round (float (variable),6)
        return [variable if type (variable) == int or  type (variable) == float else np.NaN] [0]
    except:
        variable = np.NaN
        return variable
    # if type(variable) == int or type(variable) == float:
    #     return variable
    # else:
    #     return np.NaN
def dfonlynum (df,*columns):
    for col in columns:
        df [col] = df [col].apply (onlyNum)
    return df
def NumMask (df,col,x,y):   # Select a set of numbers from a column. I used it for Ranks.
    Numberlist= [i for i in range (x,y+1)]
    mask= df [col].apply(lambda x : x in Numberlist)
    return mask
#===============================================================================
def catchpattern(df,col,mypattern):
    return df [col].apply (lambda x: re.findall(mypattern,str(x)) [0])
def splitname   (df,col,splitchar):
    return df [col].apply (lambda x : str(x).split (splitchar) [0].rstrip())     # Removing explanations (descriptions)
#===============================================================================
def print_full_rows(x):
    pd.set_option('display.max_rows', len(x))
    print(x)
    pd.reset_option('display.max_rows')
def print_full_col (x):
    pd.set_option('display.max_columns', len(x.columns))
    print(x)
    pd.reset_option('display.max_columns')
def print_full (x)   :
    pd.set_option('display.max_rows', len(x))
    pd.set_option('display.max_columns', len(x.columns))
    print(x)
    pd.reset_option('display.max_rows')
    pd.reset_option('display.max_columns')
#===============================================================================
def mymerge (df1,df2,df3,col):
    mydf = pd.merge (df1,df2, how ='inner')
    mydf2= pd.merge (mydf,df3, how = 'inner')
    return mydf2
def checkrecord (df , col , record):
    return df [col] [df[col] == record].tolist() [0]
def checkrecordinalldf (df1, df2 , df3 , col , record):
    return checkrecord (df1, col , record) == checkrecord (df2, col , record) == checkrecord (df3, col , record)
#===============================================================================
#===============================================================================
