# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 14:48:11 2021

@author: SESWARAN
"""

def addSignals(dt,param):
#%% latacc, longAcc targets
    import numpy as np
    from math import radians
    import pandas as pd

    try:
        AyP = param['AyProfile']
        #Target Lateral Acceleration - Dynamic
        dt['AyDyn'] = np.interp(dt['VmcVsevVeh'],AyP['SpeedAy'],AyP['AyD']) 
        #Target Lateral Acceleration - Comfort
        dt['AyCmf'] = np.interp(dt['VmcVsevVeh'],AyP['SpeedAy'],AyP['AyC'])
        del AyP
        
        AxpP = param['AxpProfile']
        #Target Long Acceleration - Dynamic
        dt['AxpDyn'] = np.interp(dt['VmcVsevVeh'],AxpP['speedAxp'],AxpP['AxpD']) 
        #Target Long Acceleration - Comfort
        dt['AxpCmf'] = np.interp(dt['VmcVsevVeh'],AxpP['speedAxp'],AxpP['AxpC'])  
        del AxpP
        
        AxnP = param['AxnProfile']
        #Target Long Acceleration - Dynamic
        dt['AxnDyn'] = np.interp(dt['VmcVsevVeh'],AxnP['speedAxn'],AxnP['AxnD']) 
        #Target Long Acceleration - Comfort
        dt['AxnCmf'] = np.interp(dt['VmcVsevVeh'],AxnP['speedAxn'],AxnP['AxnC']) 
        del AxnP
       
    except Exception as ex:
        print('Accel targets could not be generated due to',ex.__class__)
            
    #%% Wgs conversion, distance b/w lat long calculation
    
    try:
        #HPX,HPY to WGS
        dt['Latitude_wgs'] = dt['GPSLatitude']*10**-6 -90
        dt['Longitude_wgs'] = dt['GPSLongitude']*10**-6 -180
        
        #deg to rad conv
        Latitude_wgs_rad = dt['Latitude_wgs'].apply(lambda x:radians(x))
        Longitude_wgs_rad = dt['Longitude_wgs'].apply(lambda x:radians(x))
        
        # to calculate dist b/w shape points (same formula used in route validation as well)
        lat1 = Latitude_wgs_rad.shift(1)
        lat2 = Latitude_wgs_rad        
        lon1 = Longitude_wgs_rad.shift(1)
        lon2 = Longitude_wgs_rad                
        length = 2*6371000*(np.sqrt(np.power(np.sin((lat1-lat2)/2),2)+np.cos(lat1)*np.cos(lat2)*np.power(np.sin((lon1-lon2)/2),2)))
        length = length.fillna(0) # fill nan values with zero
        gps_distance = length.cumsum() # find the cumulative distance (running total)
       
    except Exception as ex:
        print('GPS data could not be processed due to',ex.__class__)
    
    
    #%% convert signal enumerations
    try:
        ehSpdlimValue0 = dt['EhrSpdlim_0'].map(param['map_ehrSpdlim']) # radius reported by map for current position
        #dt['ehSpdlimValue1'] = dt['EhrSpdlim_1'].map(map_ehrSpdlim) # radius reported for next shape point - not used now
        if (dt['EhrSpdlimUnits'].values[0] == 0): # 0 is KPH
            dt['ehSpdlimValue0_KPH'] = ehSpdlimValue0
        elif (dt['EhrSpdlimUnits'].values[0] == 1): # 0 is MPH
            dt['ehSpdlimValue0_MPH'] = ehSpdlimValue0
        
        
        dt['EhrRoadClass_0_Map'] = dt['EhrRoadClass_0'].map(param['map_ehrFuncRoadClass']) # functional road class enum
        
        TSRSpdLimit_int = pd.to_numeric(dt['TSRSpdLimit'],errors='coerce') # tsr speed limit non numeric will be set to nan
        if (dt['TSRSpdLimitUnits'].values[0] == 'Km/h'): 
            dt['TSRSpdLimitKPH'] = TSRSpdLimit_int        
        elif(dt['TSRSpdLimitUnits'].values[0] == 'Mph'):
                dt['TSRSpdLimitMPH'] = TSRSpdLimit_int 
        
        dt['CcfSpdoCalPercentScaleMap'] = dt['CcfSpdoCalPercentScale'].map(param['map_spdoCalPerScale']) # spd cal for ind speed 
        dt['CcfSpdoCalkmhOffsetMap'] = dt['CcfSpdoCalkmhOffset'].map(param['map_spdoCalOffset']) # spd offset for ind speed
     
    except Exception as ex:
        print('Enum mapping could not be processed due to',ex.__class__)   
    #%% Vse based  Curvature, corner target speed and Ay
    try:
        dt['curvatureVse'] = (dt['VmcVsevVeh']/3.6) / (2*np.pi*dt['PSIP1']/400) # curve radius value in m based on Yaw & speed 
        dt['AyVse'] = (2*np.pi*dt['PSIP1']/400) * (dt['VmcVsevVeh']/3.6)  # lat acc based on yaw and speed         
        # speed calculations with unfiltered curvature data
        # corner speed based on estimated curvature (Vse) in KPH
        dt['CornerTgtSpdCmf_VseUnfil_KPH'] = np.sqrt(np.abs(dt['curvatureVse']) * (dt['AyCmf']))*3.6 # comfort KPH
        dt['CornerTgtSpdDyn_VseUnfil_KPH'] = np.sqrt(np.abs(dt['curvatureVse']) * (dt['AyDyn']))*3.6 # dynamic KPH
        # corner speed based on estimated curvature (Vse) in KPH
        dt['CornerTgtSpdCmf_VseUnfil_MPH'] = np.sqrt(np.abs(dt['curvatureVse']) * (dt['AyCmf']))*3.6*0.621371 # comfort MPH
        dt['CornerTgtSpdDyn_VseUnfil_MPH'] = np.sqrt(np.abs(dt['curvatureVse']) * (dt['AyDyn']))*3.6*0.621371  # dynamic MPH
       
        # vse radius remove values above 1200m radius
        dt['curvatureVseFilt']= np.where(abs(dt['curvatureVse'])>=1200,np.nan,dt['curvatureVse'])
                                
    except Exception as ex:
        print('Corner Target speeds could not be processed due to',ex.__class__)
    #%%  E-Horizon based corner target speeds
    # try:
    # remove duplicated curvature values & unfiltered
    dt['EhrRadius0Dup'] = np.where(dt['EhrRadius_0'].eq(dt['EhrRadius_0'].shift()),0,dt['EhrRadius_0']) 
    # corner speed based on map curvature in KPH
    dt['CornerTgtSpdCmf_EhrUnfil_KPH'] = np.sqrt(np.abs(dt['EhrRadius0Dup']) * (dt['AyCmf']))*3.6 # comfort KPH
    dt['CornerTgtSpdDyn_EhrUnfil_KPH'] = np.sqrt(np.abs(dt['EhrRadius0Dup']) * (dt['AyDyn']))*3.6 # dynamic KPH
    # corner speed based on map curvature in MPH
    dt['CornerTgtSpdCmf_EhrUnfil_MPH'] = np.sqrt(np.abs(dt['EhrRadius0Dup']) * (dt['AyCmf']))*3.6*0.621371 # comfort MPH
    dt['CornerTgtSpdDyn_EhrUnfil_MPH'] = np.sqrt(np.abs(dt['EhrRadius0Dup']) * (dt['AyDyn']))*3.6*0.621371 # dynamic MPH

    # get absolute values & filter ehorizon curvature  (set values 1200 to nan) 
    dt['EhrRadius0Fil1200'] = np.where(abs(dt['EhrRadius0Dup']) >= 1200,np.nan,dt['EhrRadius0Dup'])
    # replace 0 with nan
    dt['EhrRadius0Fil1200_zero'] =  dt['EhrRadius0Fil1200'].replace(0,np.nan)
    
    # corner speed based on map curvature in KPH - Filtered
    dt['CornerTgtSpdCmf_EhrFil_KPH'] = np.sqrt(np.abs(dt['EhrRadius0Fil1200_zero']) * (dt['AyCmf']))*3.6 # comfort KPH
    dt['CornerTgtSpdDyn_EhrFil_KPH'] = np.sqrt(np.abs(dt['EhrRadius0Fil1200_zero']) * (dt['AyDyn']))*3.6 # dynamic KPH
    # corner speed based on map curvature in MPH - filtered
    dt['CornerTgtSpdCmf_EhrFil_MPH'] = np.sqrt(np.abs(dt['EhrRadius0Fil1200_zero']) * (dt['AyCmf']))*3.6*0.621371 # comfort MPH
    dt['CornerTgtSpdDyn_EhrFil_MPH'] = np.sqrt(np.abs(dt['EhrRadius0Fil1200_zero']) * (dt['AyDyn']))*3.6*0.621371 # dynamic MPH
    
    # interpolate based on distance b/e shapepoints
    EhrRadius0Intrp = pd.DataFrame(dt['EhrRadius0Dup'].values,gps_distance.values).replace(0,np.nan)
    EhrRadius0Intrp = EhrRadius0Intrp.interpolate(method='index')
    dt['EhrRadius0Intrp'] = pd.DataFrame(EhrRadius0Intrp.values,dt.index.values)
    
    # get absolute values & filter ehorizon curvature  (set values 1200 to nan) 
    dt['EhrRadius0Intrp1200'] = np.where(abs(dt['EhrRadius0Intrp']) >= 1200,np.nan,dt['EhrRadius0Intrp'])
    # replace 0 with nan
    dt['EhrRadius0Intrp1200_zero'] =  dt['EhrRadius0Intrp'].replace(0,np.nan)
    # corner target speed based on interpolated ehr curvature
     # corner speed based on map curvature in KPH - Filtered
    dt['CornerTgtSpdCmf_EhrIntrpl_KPH'] = np.sqrt(np.abs(dt['EhrRadius0Intrp1200_zero']) * (dt['AyCmf']))*3.6 # comfort KPH
    dt['CornerTgtSpdDyn_EhrIntrpl_KPH'] = np.sqrt(np.abs(dt['EhrRadius0Intrp1200_zero']) * (dt['AyDyn']))*3.6 # dynamic KPH
    # corner speed based on map curvature in MPH - filtered
    dt['CornerTgtSpdCmf_EhrIntrpl_MPH'] = np.sqrt(np.abs(dt['EhrRadius0Intrp1200_zero']) * (dt['AyCmf']))*3.6*0.621371 # comfort MPH
    dt['CornerTgtSpdDyn_EhrIntrpl_MPH'] = np.sqrt(np.abs(dt['EhrRadius0Intrp1200_zero']) * (dt['AyDyn']))*3.6*0.621371 # dynamic MPH
    
    
    # except Exception as ex:
    #     print('Filtering values could not be processed due to',ex.__class__)
    
    #%% IPMA signals   
    try:   
        dt['IpmaSignValue_0_Map'] = dt['IpmaSignValue_0'].map(param['map_ipmaSpdlim'])
        
        dt['IpmaSignOffset_0_m'] = dt['IpmaSignOffset_0'] * 0.2
        
        dt['IpmaSignPosVariance_0_m2'] = dt['IpmaSignPosVariance_0'] * 0.25
        
    except Exception as ex:
        print('IPMA signal values could not be processed due to',ex.__class__)
    #%%
    try:
        # calculate speed caibration for cluster
        dt['IndVehicleSpeedKPH'] = (dt['VehicleSpeed'] * 8000 / dt['CcfTyreSizeCorrnFac'] * (1+dt['CcfSpdoCalPercentScaleMap']))+dt['CcfSpdoCalkmhOffsetMap']
        dt['IndVehicleSpeedMPH'] = dt['IndVehicleSpeedKPH'] * 0.621371 

        dt['IndCornerTgtSpdCmf_EhrFil_MPH'] = (dt['CornerTgtSpdCmf_EhrFil_MPH'] * 8000 / dt['CcfTyreSizeCorrnFac'] * (1+dt['CcfSpdoCalPercentScaleMap']))+dt['CcfSpdoCalkmhOffsetMap']
        
        
        
    except Exception as ex:
        print('Display values could not be processed due to',ex.__class__)
#%%        
    return dt


