#%% Load Libraries
from mf4parser import mdfSubset as ms
import pandas as pd
from time import sleep
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
from scipy import interpolate
import inputFunc
import addSignals
#%% User Inputs and Load parameters

srcFiles,csvpath,ts = inputFunc.getinput()
param = inputFunc.loadparam()

#%% Create Subsets list from MF4s
subset =[]
for files in range(len(srcFiles)): #
    print(f'\nRead mf4 files started. {files+1}/{len(srcFiles)} File selected {srcFiles[files].name}')
    sleep(1)
    subset.append(ms.createSubset(str(srcFiles[files]), csvpath))
    print('File reading completed')
    sleep(1)

#%% create data table
dt = [subsets.createDataTable(ts) for subsets in subset]
    
#%% generate additional signals
# dt_add = [addSignals.addSignals(dt, param) for tab in dt]
dt_add=[]
for frame in range(len(dt)):
    dt_add.append(addSignals.addSignals(dt[frame],param))
    
#%%
for frames in range(len(dt_add)):
    fname = srcFiles[0].parent.as_posix().replace('/','\\')+'\\'+subset[frames].name+'.csv'
    dt_add[frames].to_csv(fname,index_label='timestamps')  
    print(f'CSV Files created successfully for file {subset[frames].name}')


# %%
