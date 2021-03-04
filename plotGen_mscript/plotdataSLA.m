%% Plotting data - Plot 1 CSA - HMI View
plots = figure;
plots.WindowState = 'maximized';

tiledlayout(7,1)
nexttile
plot(ts,accTsr)
title('ACC TSR Follow Status')

nexttile
plot(ts,currentSLsign,'b',ts,eHSL,'m--')
title('TSR SL Vs EHR SL')
legend('CurrSL','EHR SL','location','eastoutside')


nexttile([2 1])
plot(ts,setspdInd,'b',ts,currentSLsign,'m:',ts,vehSpdIndMph,'r')
ylabel('Vx in MPH')
title('SetSpeedDADC Vs Speed Limit Vs Ind. Vehicel Speed (IN MPH - Indicated)')
legend('DispSetSpeed','Current SL','IndicatedVmcVeh','location','eastoutside')

nexttile
plot(ts,Spdribbon,'--')
title('Adaptive Ribbon ')

nexttile
plot(ts,nextSLsign)
title('Next SL sign in the cluster')

nexttile
plot(ts,craIcon)
title('Adaptation Icon (10 - CSA Icon; 20 - SLA Icon)')
%%
fn = split(fname,'.');
figname = string(path)+'\'+string(fn(1))+'_SLA_HMI.fig';
savefig(figname)
jpgname = string(path)+'\'+string(fn(1))+'_SLA_HMI.jpg';
saveas(gcf,jpgname);

close all
%% Plotting data - Plot 1 CSA - Motion View
plots = figure;
plots.WindowState = 'maximized';

tiledlayout(7,1)
nexttile
plot(ts,accTsr)
title('TSR Status')

nexttile([2 1])
plot(ts,vmcSpdKph,'r',ts,setspdKph,'b')
ylabel('Vx in KPH')
title('Vehicle Speed Vs SetSpeed ')
legend('VmcVehV','SetSpeedCC','location','eastoutside')

nexttile([2 1])
plot(ts,setspdInd,'b',ts,Spdribbon,'--',ts,currentSLsign,'m:',ts,vehSpdIndMph,'r')
ylabel('Vx in MPH')
title('SetSpeedDADC Vs Adaptive Ribbon Vs Speed Limit Vs Ind. Vehicel Speed (IN MPH - Indicated)')
legend('DispSetSpeed','Ribbon','Current SL','IndicatedVmcVeh','location','eastoutside')

nexttile([2 1])
plot(ts,AxReq,'r--',ts,VseAx,'b',ts,AxNCmf,ts,AxPCmf)
ylabel('Ax in mps2')
title('Ax Request Vs Ax OverGround Vs Decel Limit Vs Ax Limit')
legend('DADCAxReq','AxOverGrd','Decel Limit','Accel Limit','location','eastoutside')


%%
fn = split(fname,'.');
figname = string(path)+'\'+string(fn(1))+'_SLA_Motion.fig';
savefig(figname)
jpgname = string(path)+'\'+string(fn(1))+'_SLA_Motion.jpg';
saveas(gcf,jpgname);

close all