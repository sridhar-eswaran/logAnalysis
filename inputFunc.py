# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 11:31:20 2021

@author: SESWARAN
"""



# User input function
def getinput():
    from tkinter import Tk,filedialog,simpledialog,messagebox
    import pathlib
    gui = Tk()
    gui.withdraw()
    #os.system('cls')
    path = filedialog.askdirectory(title='Select Folder')
    srcFiles = list(pathlib.Path(path).glob('*.mf4'))

    csv = filedialog.askopenfile(title='Choose signal list CSV file').name

    ts = simpledialog.askfloat('Input resample timestep',"Enter resampling frequency in seconds:\n \
                                          Min: 0.01 (10ms) & Max: 1(1sec) \n e.g.20ms is 0.02",minvalue=0.01,maxvalue=1)
    # Warning for loading too many files
    if len(srcFiles) > 10:
        response = messagebox.askyesno(title='Too many Files', message='Loading more than 10 files at once might slow down the computer. Do you want to proceed?')
        if response is False:
            quit()
            
    return srcFiles,csv,ts

def loadparam():
    import json
    #load parameters from JSON
    with open('C:/Users/seswaran/Documents/PyWorkspace/PyFiles_git/logAnalysis/parameters_dict.json') as f:
      param = json.load(f)
    return param   
