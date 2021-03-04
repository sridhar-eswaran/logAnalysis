%% Get the folder from user
path = uigetdir();

%% Get the csv files from the selected folder
flist = dir(string(path)+'\*.csv');

%% read CSV files and generate fig and pngs
for fnum=1:length(flist)
    fpath = string(path)+'\'+string(flist(fnum).name);
    fname = flist(fnum).name;
    
    data = readtable(fpath);
    
    run signalAbstraction.m
    run plotdataCSA.m
    run plotdataSLA.m
    run plotRoute.m
    
end