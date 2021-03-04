
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