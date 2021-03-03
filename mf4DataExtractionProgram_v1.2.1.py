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

#%%

# data = pd.read_csv('20210218T162440Z_DASy_003.csv',index_col='timestamps')
# dt = dt[0]
# data.loc[data['CornerTgtSpdCmf_Ehr_MPH'] ==0,'CornerTgtSpdCmf_Ehr_MPH'] = np.nan
# maxYlim = max(data['DisplaySetSpeedDADC']) + 30
# data.loc[data['CornerTgtSpdCmf_Ehr_MPH'] > maxYlim,'CornerTgtSpdCmf_Ehr_MPH'] = np.nan



# corspdNotZero = (data['CornerTgtSpdCmf_Ehr_MPH'] != 0)
# maxYlim = max(data['DisplaySetSpeedDADC']) + 30

# maxSL = int(max(data['TSRSpdLimit']))
# upperSpdLim = max(maxSpd,maxSL)+20
# corspdLessmax = (data['CornerTgtSpdCmf_Ehr_MPH'] < upperSpdLim)
# corspdNotzeroLessmax = corspdNotZero & corspdLessmax
# corspdNotzeroLessmax = data.loc[corspdNotZero & corspdLessmax]

# #%% Abstract signals for plot
# # get column names from the data frame
# columnN = pd.Series(dt_add[1].columns.values).to_csv('columnnames.csv')

# #%% Plotting
# mpl.rcParams['lines.linewidth']=0.2


# for frames in range(1):#len(dt_add)
#     data = dt_add[frames]
#     # VseVeh_KPH = data['VmcVsevVeh']
#     # VseVeh_MPH = data['VmcVsevVeh']*0.621371
#     # IndVseVeh_KPH = data['IndVehicleSpeedKPH']
#     # IndVseVeh_MPH = data['IndVehicleSpeedMPH']
    
#     data_AccActive = data.mask(data['ACCStatus']!='FOLLOWMODE')
#     data_AccStandby = data.mask(data['ACCStatus']!='STANDBYMODE')
#     data_AccOverride = data.mask(data['ACCStatus']!='OVERRIDE')
    
#     data_AyHigh = data.mask(abs(data['AyVse']) < data['AyCmf']+1)
#     data_AyMid = data.mask((abs(data['AyVse']) <= data['AyCmf']-1) & (abs(data['AyVse']) >= data['AyCmf']+1))
#     data_AyLow = data.mask(abs(data['AyVse']) > data['AyCmf']-1)
    
#     Cspeed_eh_KPH = data.mask(data['IndCornerTgtSpdCmf_EhrFil_MPH'] > max(data['VmcVsevVeh'])+20)
#     # Masks needed
#     # ACC status
#     # TSR status
#     # Corner Speed < vehicle speed
#     # AyVse < AyCmf
    
    
    
    
    # # ev speed masking
    # VseVeh_KPH_act = data_AccActive['VmcVsevVeh']
    # VseVeh_KPH_std = data_AccStandby['VmcVsevVeh']
    # VseVeh_KPH_ovr = data_AccOverride['VmcVsevVeh']
    
    # plt.subplot(2,1,1)
    # plt.plot(VseVeh_KPH_act,label='Ev Speed KPH - ACC Active',color='g')
    # plt.plot(VseVeh_KPH_std,label='Ev Speed KPH - ACC Standby',color='r')
    # plt.plot(VseVeh_KPH_ovr,label='Ev Speed KPH - ACC Override',color='m')
    # plt.title('Speed Vs Time',loc='left')
    # plt.grid()
    # plt.xlabel('timestamps')
    # plt.ylabel('Speed in KPH')
    # plt.scatter(Cspeed_eh_KPH.index,Cspeed_eh_KPH.values,marker='+',color='b',label = 'Corner target Speed KPH',linewidths=0.1)
    
    
    
    # plt.subplot(2,1,2)
    # plt.plot(data_AyHigh['AyVse'],color='r')
    # plt.plot(data_AyMid['AyVse'],color='y')
    # plt.plot(data_AyLow['AyVse'],color='g')
    # plt.grid()
    
    # #plt.savefig('destination_path.png', format='png',dpi=1200)
    # plt.show()

