# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 15:49:05 2021

@author: SESWARAN

"""
import numpy as np
import json
params = {
    
    "AyProfile" : {
        "SpeedAy":[0,16,64,96,200,1000], #in kph
        "AyD" : [4.5,4.5,4.5,3.2,3.2,0],
        "AyC" : [3.4,3.4,3.4,2.4,2.4,0],
        "AyE" : [3.4,3.4,3.4,2.4,2.4,0]
        },
    "AxpProfile" : {
        "speedAxp" : [0,40,140,200,1000], #in kph
        "AxpD" : [1.07,1.56,1.07,0.42,0],
        "AxpC" : [0.93,1.22,0.72,0.31,0],
        "AxpE" : [0.79,0.87,0.37,0.22,0]
        },
    "AxnProfile" : {
        "speedAxn" : [0,3,10,40,140,200,1000], #in kph
        "AxnD" : [-0.5,-0.5,-1.5,-2.2,-1.5,-0.7,0],
        "AxnC" : [-0.5,-0.5,-1.3,-1.85,-1.15,-0.5,0],
        "AxnE" : [-0.5,-0.5,-1.1,-1.5,-0.8,-0.3,0]
        },

    "map_ehrSpdlim" : {
            0:0,1:5,2:7,3:10,4:15,5:20,6:25,7:30,8:35,9:40,10:45,11:50,12:55,13:60,14:65,15:70,16:75,17:80,18:85,19:90,20:95,
            21:100,22:105,23:110,24:115,25:120,26:130,27:140,28:150,29:200,30:200,31:0
            },
        
    "map_ipmaSpdlim" : {
            0:0,1:5,2:10,3:15,4:20,5:25,6:30,7:35,8:40,9:45,10:50,11:55,12:60,13:65,14:70,15:75,16:80,17:85,18:90,19:95,20:100,
            21:105,22:110,23:115,24:120,25:125,26:130,27:135,28:140,29:145,30:150,31:155,32:160
            },
    
    "map_spdoCalPerScale" : {
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
            },
        
        #CcfSpdoCalkmhOffsetCoding
    "map_spdoCalOffset" : {
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
            },
        
        #FunctionalRoadClass
    "map_ehrFuncRoadClass" : {
            0:0,
            1:0,
            2:1,
            4:2,
            8:3,
            16:4,
            32:5,
            64:0,
            128:0
            },
        
        #speedLimitType
    "map_ehrSpdLimType" : {
            0:'Implicit',
            1:'Explicit:TrafficSign',
            2:'Explicit:Night',
            3:'Explicit:Day',
            4:'Explicit:TimeOfDay',
            5:'Explicit:Rain',
            6:'Explicit:Snow',
            7:'Unknown'
            },
        
        #FormOfWay
    "map_ehrFormOfWay" : {
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
            },
        
        #Complex Intersection
    "map_ehrInterSec" : {
            0:'NotComplexIntersection',
            1:'ComplexIntersection',
            2:'Unknown',
            3:'N/A'
            },
        
        #RightofWay
    "map_ehrRightofWay" : {
            0:'HostVehicle',
            1:'OtherVehicle',
            2:'Unknown',
            3:'N/A'
            },
    #Units of speed limit values reported by EHR data
    "map_ehrSpdlimUnits" : {
            0:'mph',
            1:'km/h',
            }
}

with open('parameters_dict.json', 'w') as f:
    json.dump(params, f)

