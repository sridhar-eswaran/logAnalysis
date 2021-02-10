#%%
from mf4parser import mdfSubset as ms
from tkinter import Tk,filedialog,simpledialog
import pandas as pd
import pathlib
from time import sleep
import numpy as np
from matplotlib import pyplot as plt
#%%
gui = Tk()
gui.withdraw()
#os.system('cls')
def getMf4Files():
    path = filedialog.askdirectory(title='Select Folder')
    files = list(pathlib.Path(path).glob('*.mf4'))
    return files

def getCsvFilepath():
    csv = filedialog.askopenfile(title='Choose signal list CSV file').name
    return csv
    
def getSampleTimestep():
    value = simpledialog.askfloat('Input resample timestep',"Enter resampling frequency in seconds:\n \
                                          Min: 0.01 (10ms) & Max: 1(1sec) \n e.g.20ms is 0.02",minvalue=0.01,maxvalue=1)
    return value


srcFiles = getMf4Files()
csvpath = getCsvFilepath()
ts = getSampleTimestep()

def loadAyprofile():
    # Lateral accelration profiles
    AyProfile = {
        "SpeedAy":[0,16,64,96,200,1000], #in kph
        "AyD" : [4.5,4.5,4.5,3.2,3.2,0],
        "AyC" : [3.4,3.4,3.4,2.4,2.4,0],
        "AyE" : [3.4,3.4,3.4,2.4,2.4,0]
        }
    return AyProfile

def loadAxpprofile():
    # Longitudinal accelration profiles
    AxpProfile = {
        "speedAxp" : [0,40,140,200,1000], #in kph
        "AxpD" : [1.07,1.56,1.07,0.42,0],
        "AxpC" : [0.93,1.22,0.72,0.31,0],
        "AxpE" : [0.79,0.87,0.37,0.22,0]
        }
    return AxpProfile

def loadAxnprofile():
    # Longitudinal decelration profiles
    AxnProfile = {
        "speedAxn" : [0,3,10,40,140,200,1000], #in kph
        "AxnD" : [-0.5,-0.5,-1.5,-2.2,-1.5,-0.7,0],
        "AxnC" : [-0.5,-0.5,-1.3,-1.85,-1.15,-0.5,0],
        "AxnE" : [-0.5,-0.5,-1.1,-1.5,-0.8,-0.3,0]
        }
    return AxnProfile

# Enumeration definitions
# Ehorizon Speed limit
map_ehrSpdlim = {
    0:0,1:5,2:7,3:10,4:15,5:20,6:25,7:30,8:35,9:40,10:45,11:50,12:55,13:60,14:65,15:70,16:75,17:80,18:85,19:90,20:95,
    21:100,22:105,23:110,24:115,25:120,26:130,27:140,28:150,29:200,30:200,31:0
    }

# CcfSpdoCalPercentScaleCoding
map_spdoCalPerScale = {
    'Not supported':np.nan,
    '0.0% Scaling':0,
    '0.5% Scaling':0.005,
    '1.0% Scaling':0.01,
    '1.5% Scaling':0.015,
    '2.0% Scaling':0.020,
    '2.5% Scaling':0.025,
    '3.0% Scaling':0.030,
    '3.5% Scaling':0.035,
    '4.0% Scaling':0.040,
    '4.5% Scaling':0.045,
    '5.0% Scaling':0.050,
    '5.5% Scaling':0.055,
    '6.0% Scaling':0.060,
    '6.5% Scaling':0.065,
    '7.0% Scaling':0.070,
    '7.5% Scaling':0.075,
    'Error':np.nan
    }

#CcfSpdoCalkmhOffsetCoding
map_spdoCalOffset = {
    'Not supported':np.nan,
    '+ 0.0 km/h':0,
    '+ 0.5 km/h':0.5,
    '+ 1.0 km/h':1.0,
    '+ 1.5 km/h':1.5,
    '+ 2.0 km/h':2.0,
    '+ 2.5 km/h':2.5,
    '+ 3.0 km/h':3.0,
    '+ 3.5 km/h':3.5,
    'Error':np.nan
    }

#FunctionalRoadClass
map_ehrFuncRoadClass = {
    0:0,
    1:0,
    2:1,
    4:2,
    8:3,
    16:4,
    32:5,
    64:0,
    128:0
    }

#speedLimitType
map_ehrSpdLimType = {
    0:'Implicit',
    1:'Explicit:TrafficSign',
    2:'Explicit:Night',
    3:'Explicit:Day',
    4:'Explicit:TimeOfDay',
    5:'Explicit:Rain',
    6:'Explicit:Snow',
    7:'Unknown'
    }

#FormOfWay
map_ehrFormOfWay = {
    0:'Unknown',
    1:'Freeway/ControlledAccess',
    2:'MulitipleCarriageWay',
    3:'SingleCarriageWay',
    4:'Roundabout',
    5:'TrafficSquare',
    6:'Reserved',
    7:'Reserved',
    8:'ParallelRoad',
    9:'SlipRoad/Ramp_FreeWay/ControlledAccess',
    10:'SlipRoad/Ramp_Non-FreeWay',
    11:'ServiceRoad',
    12:'Entry/Exit_CarPark',
    13:'Entry/Exit_Service',
    14:'PedestrianZone',
    15:'N/A'
    }

#Complex Intersection
map_ehrInterSec = {
    0:'NotComplexIntersection',
    1:'ComplexIntersection',
    2:'Unknown',
    3:'N/A'
    }

#RightofWay
map_ehrRightofWay = {
    0:'HostVehicle',
    1:'OtherVehicle',
    2:'Unknown',
    3:'N/A'
    }


def addSignals(dt):
    #HPX,HPY to WGS
    dt['Latitude_wgs'] = dt['GPSLatitude']*10**-6 -90
    dt['Longitude_wgs'] = dt['GPSLongitude']*10**-6 -180
    
    AyP = loadAyprofile()
    #Target Lateral Acceleration - Dynamic
    dt['AyDyn'] = np.interp(dt['VmcVsevVeh'],AyP['SpeedAy'],AyP['AyD']) 
    #Target Lateral Acceleration - Comfort
    dt['AyCmf'] = np.interp(dt['VmcVsevVeh'],AyP['SpeedAy'],AyP['AyC'])
    
    # Measured Curvature Value
    dt['curvatureVse'] = abs((dt['VmcVsevVeh']/3.6) / (2*np.pi*dt['PSIP1']/400))
    dt['curvatureVseFilt']= np.where(dt['curvatureVse']>=1500,1500,dt['curvatureVse'])
    dt['curvatureVseFilt']= np.where(dt['curvatureVse']<=-1500,-1500,dt['curvatureVse'])
    
    # measured lateral Acceleration value
    dt['AyVse'] = abs((2*np.pi*dt['PSIP1']/400) * (dt['VmcVsevVeh']/3.6))
    
    # Difference b/w A1 & Measured lat acc
    dt['Aydiff_A1_AyVse'] = dt['A1'] - (dt['AyVse'])
    
    # Difference b/w comfort target & A1
    dt['Aydiff_Cmf_A1'] = dt['AyCmf'] - (dt['A1'])
    # Difference b/w Dynamic target & A1
    dt['Aydiff_Dyn_A1'] = dt['AyDyn'] - (dt['A1'])
    
    # Difference b/w comfort target & Measured lat acc
    dt['Aydiff_Cmf_AyVse'] = dt['AyCmf'] - (dt['AyVse'])
    # Difference b/w Dynamic target & Measured lat acc
    dt['Aydiff_Dyn_AyVse'] = dt['AyDyn'] - (dt['AyVse'])
    
    # Convert enumerated values to speed values - Ehorizon
    dt['ehSpdlimValue0'] = dt['EhrSpdlim_0'].map(map_ehrSpdlim)
    dt['ehSpdlimValue1'] = dt['EhrSpdlim_1'].map(map_ehrSpdlim)
        
    # Remove duplicated curvature values and satureate the curvature values above 1500 to 1500
    dt['EhrRadius0Fil'] = np.where(dt['EhrRadius_0'].eq(dt['EhrRadius_0'].shift()),0,dt['EhrRadius_0'])
    dt['EhrRadius0Fil'] = np.where(dt['EhrRadius0Fil']>=1500,1500,dt['EhrRadius0Fil'])
    dt['EhrRadius0Fil'] = np.where(dt['EhrRadius0Fil']<=-1500,-1500,dt['EhrRadius0Fil'])

    # CcfSpdoCalPercentScale mapping
    dt['CcfSpdoCalPercentScaleMap'] = dt['CcfSpdoCalPercentScale'].map(map_spdoCalPerScale)

    # CcfSpdoCalkmhOffset
    dt['CcfSpdoCalkmhOffsetMap'] = dt['CcfSpdoCalkmhOffset'].map(map_spdoCalOffset)


    # Indicated vehicle speed
    dt['IndVehicleSpeedKPH'] = (dt['VehicleSpeed'] * 8000 / dt['CcfTyreSizeCorrnFac'] * (1+dt['CcfSpdoCalPercentScaleMap']))+dt['CcfSpdoCalkmhOffsetMap']
    dt['IndVehicleSpeedMPH'] = dt['IndVehicleSpeedKPH'] * 0.621371 
    
    # Corner target Speed - Ehorizon Radius based    
    dt['CornerTgtSpdCmf_Ehr_KPH'] = np.sqrt(np.abs(dt['EhrRadius0Fil']) * (dt['AyCmf']))*3.6
    dt['CornerTgtSpdDyn_Ehr_KPH'] = np.sqrt(np.abs(dt['EhrRadius0Fil']) * (dt['AyDyn']))*3.6
    
    #Corner Target Speed - Vse Radius
    dt['CornerTgtSpdCmf_Vse_KPH'] = np.sqrt(np.abs(dt['curvatureVseFilt']) * (dt['AyCmf']))*3.6
    dt['CornerTgtSpdDyn_Vse_KPH'] = np.sqrt(np.abs(dt['curvatureVseFilt']) * (dt['AyDyn']))*3.6
    
    # Corner target Speed - Ehorizon Radius based    
    dt['CornerTgtSpdCmf_Ehr_MPH'] = np.sqrt(np.abs(dt['EhrRadius0Fil']) * (dt['AyCmf']))*3.6* 0.621371 
    dt['CornerTgtSpdDyn_Ehr_MPH'] = np.sqrt(np.abs(dt['EhrRadius0Fil']) * (dt['AyDyn']))*3.6* 0.621371 
    
    #Corner Target Speed - Vse Radius
    dt['CornerTgtSpdCmf_Vse_MPH'] = np.sqrt(np.abs(dt['curvatureVseFilt']) * (dt['AyCmf']))*3.6* 0.621371 
    dt['CornerTgtSpdDyn_Vse_MPH'] = np.sqrt(np.abs(dt['curvatureVseFilt']) * (dt['AyDyn']))*3.6* 0.621371 
    
    dt['TSRSpdLimit_int'] = pd.to_numeric(dt['TSRSpdLimit'],errors='coerce')
    
    return dt
    
#%% Create Subsets list from MF4s
subset =[]
for files in range(len(srcFiles)): #
    print(f'\nRead mf4 files started. File selected {srcFiles[files].name}')
    sleep(1)
    subset.append(ms.createSubset(str(srcFiles[files]), csvpath))
    print('File reading completed')
    sleep(1)

#%% create data table
dt = [subsets.createDataTable(ts) for subsets in subset]
#%% generate additional signals
dt_add = []
for frame in range(len(dt)):
    dt_add.append(addSignals(dt[frame]))
#%%
for frames in range(len(dt_add)):
    fname = srcFiles[0].parent.as_posix().replace('/','\\')+'\\'+subset[frames].name+'.csv'
    dt_add[frames].to_csv(fname,index_label='timestamps')  
    print(f'CSV Files created successfully for file {subset[frames].name}')

#%%



