%% signal abstraction
ts = data.timestamps; % timestamps
accstatus = categorical(data.ACCStatus); % acc operating status
currentSLsign = categorical(data.TSRSpdLimit); % current speed limit value
currentSLsign(currentSLsign == 'No display') = '0'
currentSLsign = double(string(currentSLsign))
nextSLsign = categorical(data.SpeedLimitNext); % next speed limit sign in the cluster
%eHSL = data.ehSpdlimValue0 % data.ehSpdlimValue0_MPH; % speed limit reported by Ehorizon  data.ehSpdlimValue0
enumEHRSL = [0;1;2;3;4;5;6;7;8;9;10;11;12;13;14;15;16;17;18;19;20;21;22;23;24;25;26;27;28;29;30;31];
valueEHRSL = [0;0;5;10;15;20;25;30;35;40;45;50;55;60;65;70;75;80;85;90;95;100;105;110;115;120;125;130;135;140;145;150];
eHSL = interp1(enumEHRSL,valueEHRSL,data.EhrSpdlim_0);
%
tsrStatus = categorical(data.TSROperatingStatus); % tsr operating status
vmcSpdKph = data.VmcVsevVeh; % vehicle speed KPH
vmcSpdMph = data.VmcVsevVeh*0.621; % vehicle speed in mph
setspdKph = data.SetspeedCC; % cruise set speed in KPH
setspdMph = data.SetspeedCC*0.621; % cruise set speed in MPH
setspdInd = data.DisplaySetSpeedDADC; % indicated set speed in the cluster
vehSpdIndKPH = data.IndVehicleSpeedKPH; % indicated vehicle speed cluster KPH
vehSpdIndMph = data.IndVehicleSpeedMPH;  % indicated vehicle speed cluster MPH
craIcon = data.CRADistToBrakingPoint; % CRA icon 10- CSA & 20 -SLA
lvpresent = categorical(data.LeadVehicleDetected); % Lead vehicel present status
AyVse = data.AyVse; % lateral acceleration of the vehicle estimated from Yaw and speed
AyCmf = data.AyCmf; % target lateral acceleration for CRA from LUT
cornerSpdEHrKPH = data.CornerTgtSpdCmf_EhrFil_KPH; % corner target speed calcualted based on Ehr curvature
cornerSpdVseKPH = data.CornerTgtSpdCmf_VseUnfil_KPH; % corner speed based on yaw and speed
Spdribbon = data.CRADisplayCornerSpd; % adaptive speed ribbon in the speed dial
VseAx = data.VmcVseAxOvrGrnd; % ax over ground vse
AxReq = data.DADCAxReq; % ax req from DADC
AxPCmf = data.AxpCmf; % accel limit
AxNCmf = data.AxnCmf; % decel limit
%%
spdmax = max(max(max(currentSLsign),max(setspdKph)),max(vmcSpdKph))+20;
cornerSpdEHrKPH(cornerSpdEHrKPH>spdmax)=NaN;

accstatus((accstatus == 'FOLLOWMODE') & (lvpresent == 'DETECTED')) = 'FM LV';
accstatus((accstatus == 'FOLLOWMODE') & (lvpresent == 'OFF')) = 'FM NO LV';
% accstatus((accstatus == 'STANDBY') & (lvpresent == 'DETECTED')) = 'STDBY LV';
% accstatus((accstatus == 'STANDBY') & (lvpresent == 'OFF')) = 'STDBY NO LV';
% accstatus((accstatus == 'OVERRIDE') & (lvpresent == 'DETECTED')) = 'OVERRIDE LV';
% accstatus((accstatus == 'OVERRIDE') & (lvpresent == 'OFF')) = 'OVERRIDE NO LV';
accstatus = categorical(string(accstatus));

tsrStatus((accstatus == 'FM LV') & (tsrStatus == 'Operating: Fusion mode' )) = 'FUSION FOLLOW LV';
tsrStatus((accstatus == 'FM NO LV') & (tsrStatus == 'Operating: Fusion mode' )) = 'FUSION FOLLOW NO LV';
tsrStatus((accstatus == 'STANDBYMODE') & (tsrStatus == 'Operating: Fusion mode' )) = 'FUSION STANDBY';
tsrStatus((accstatus == 'OVERRIDE') & (tsrStatus == 'Operating: Fusion mode' )) = 'FUSION OVERRIDE';

tsrStatus((accstatus == 'FM LV') & (tsrStatus == 'Operating: Vision only mode' )) = 'VISION FOLLOW LV';
tsrStatus((accstatus == 'FM NO LV') & (tsrStatus == 'Operating: Vision only mode' )) = 'VISION FOLLOW NO LV';
tsrStatus((accstatus == 'STANDBYMODE') & (tsrStatus == 'Operating: Vision only mode' )) = 'VISION STANDBY';
tsrStatus((accstatus == 'OVERRIDE') & (tsrStatus == 'Operating: Vision only mode' )) = 'VISION OVERRIDE';

tsrStatus((accstatus == 'FM LV') & (tsrStatus == 'Operating: Navigation only mode' )) = 'NAV FOLLOW LV';
tsrStatus((accstatus == 'STANDBYMODE') & (tsrStatus == 'Operating: Vision only mode' )) = 'NAV STANDBY';
tsrStatus((accstatus == 'OVERRIDE') & (tsrStatus == 'Operating: Vision only mode' )) = 'NAV OVERRIDE';

tsrStatus((accstatus == 'FM LV') & (tsrStatus == 'Country Not Supported' )) = 'CNS FOLLOW LV';
tsrStatus((accstatus == 'STANDBYMODE') & (tsrStatus == 'Country Not Supported' )) = 'CNS STANDBY';
tsrStatus((accstatus == 'OVERRIDE') & (tsrStatus == 'Country Not Supported' )) = 'CNS OVERRIDE';

tsrStatus((accstatus == 'FM LV') & (tsrStatus == 'Fault' )) = 'FAULT FOLLOW LV';
tsrStatus((accstatus == 'STANDBYMODE') & (tsrStatus == 'Fault' )) = 'FAULT STANDBY';
tsrStatus((accstatus == 'OVERRIDE') & (tsrStatus == 'Fault' )) = 'FAULT OVERRIDE';
accTsr = categorical(string(tsrStatus));