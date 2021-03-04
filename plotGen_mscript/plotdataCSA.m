%% Plotting data - Plot 1 CSA - HMI View
plots = figure;
plots.WindowState = 'maximized';

tiledlayout(8,1)
nexttile
plot(ts,accTsr)
title('TSR Status')

nexttile([2 1])
plot(ts,AyVse,'b',ts,AyCmf,'g',ts,AyCmf-1,'y',ts,AyCmf+1,'r')
ylabel('Ay in m/s2')
title('Lateral Accerlation Vs Limits')
legend('Measured Ay','Comfort Target','Cmf -1','Cmf+1','location','eastoutside')

nexttile([2 1])
plot(ts,vmcSpdKph,'r',ts,setspdKph,'b',ts,cornerSpdEHrKPH,'k+')
ylabel('Vx in KPH')
title('Vehicle Speed Vs SetSpeed Vs Corner Target Speed (IN KPH)')
legend('VmcVehV','SetSpeedCC','CornerSpd','location','eastoutside')

nexttile([2 1])
plot(ts,setspdInd,'b',ts,Spdribbon,'--',ts,currentSLsign,'m:',ts,vehSpdIndMph,'r')
ylabel('Vx in MPH')
title('SetSpeedDADC Vs Adaptive Ribbon Vs Speed Limit Vs Ind. Vehicel Speed (IN MPH - Indicated)')
legend('DispSetSpeed','Ribbon','Current SL','IndicatedVmcVeh','location','eastoutside')

nexttile
plot(ts,craIcon)
title('Adaptation Icon (10 - CSA Icon; 20 - SLA Icon)')

fn = split(fname,'.');
figname = string(path)+'\'+string(fn(1))+'_CSA_HMI.fig';
savefig(figname)
jpgname = string(path)+'\'+string(fn(1))+'_CSA_HMI.jpg';
saveas(gcf,jpgname);

close all
%% Plotting data - Plot 1 CSA - Motion View
plots = figure;
plots.WindowState = 'maximized';

tiledlayout(8,1)
nexttile
plot(ts,accTsr)
title('TSR Status')

nexttile([2 1])
plot(ts,AyVse,'b',ts,AyCmf,'g',ts,AyCmf-1,'y',ts,AyCmf+1,'r')
ylabel('Ay in m/s2')
title('Lateral Accerlation Vs Limits')

nexttile([2 1])
plot(ts,vmcSpdKph,'r',ts,setspdKph,'b',ts,cornerSpdEHrKPH,'k+')
ylabel('Vx in KPH')
title('Vehicle Speed Vs SetSpeed Vs Corner Target Speed (IN KPH)')
legend('VmcVehV','SetSpeedCC','CornerSpd','location','eastoutside')

nexttile([2 1])
plot(ts,AxReq,'r--',ts,VseAx,'b',ts,AxNCmf,ts,AxPCmf)
ylabel('Ax in mps2')
title('Ax Request Vs Ax OverGround Vs Decel Limit Vs Ax Limit')
legend('DADCAxReq','AxOverGrd','Decel Limit','Accel Limit','location','eastoutside')

nexttile
plot(ts,setspdInd,'b',ts,Spdribbon,'--',ts,currentSLsign,'m:',ts,vehSpdIndMph,'r')
ylabel('Vx in MPH')
title('SetSpeedDADC Vs Adaptive Ribbon Vs Speed Limit Vs Ind. Vehicel Speed (IN MPH - Indicated)')
legend('DispSetSpeed','Ribbon','Current SL','IndicatedVmcVeh','location','eastoutside')

fn = split(fname,'.');
figname = string(path)+'\'+string(fn(1))+'_CSA_Motion.fig';
savefig(figname)
jpgname = string(path)+'\'+string(fn(1))+'_CSA_Motion.jpg';
saveas(gcf,jpgname);

close all
%% Plot Route
plots = figure;
plots.WindowState = 'maximized';

geoplot(data.Latitude_wgs,data.Longitude_wgs)

fn = split(fname,'.');
figname = string(path)+'\'+string(fn(1))+'_Route.fig';
savefig(figname)
jpgname = string(path)+'\'+string(fn(1))+'_Route.jpg';
saveas(gcf,jpgname);

close all