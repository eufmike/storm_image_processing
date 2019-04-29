%% Define the path of folders
close all;
% par
pixelsize = 160;
framesize = 30;
padsize = 0;


folder_path = '/Volumes/LaCie_DataStorage/xiaochao_wei_STORM imaging/STORM_imaging/';
analysis_dir = 'analysis_20190308';
st_dir = 'spacial_test';
ip_dir = 'spacialdata_local'; % specify the input folder
op_dir = 'spacialdata_local_int';
par_dir = 'par'
csv_data = 'cropsize.csv'


% create path
ip_path = fullfile(folder_path, analysis_dir, st_dir, ip_dir);
op_path = fullfile(folder_path, analysis_dir, st_dir, op_dir);
csv_path = fullfile(folder_path, analysis_dir, par_dir, csv_data);

if ~exist(op_path)
    mkdir(op_path);
end

input = dir(ip_path);
filelist = {input.name};
filelist = filelist(~ismember(filelist, {'.', '..'}));
display(filelist);

for i = 1: length(filelist)
    path_tmp = fullfile(op_path, filelist{i})
    mkdir(path_tmp)
end

% prepare input and optput filenames
ipfilelist = {};
opfilelist = {};
for i = 1:numel(filelist)
    subfilelist_tmp = dir(fullfile(ip_path, filelist{i}, '*.csv'));
    subfilelist_name = {subfilelist_tmp.name};
    subfilelist_dir = {subfilelist_tmp.folder};
    subfilelist_name = subfilelist_name(~ismember(subfilelist_name, {'.', '..'}));
    subfilelist_dir = subfilelist_dir(~ismember(subfilelist_name, {'.', '..'}));
    
    display(size(subfilelist_name));
    display(size(subfilelist_dir));
    
    ipfilelist = [ipfilelist, fullfile(subfilelist_dir, subfilelist_name)]
    opfilelist = [opfilelist, fullfile(op_path, filelist{i}, subfilelist_name)]
    
end

display(ipfilelist{1});
display(opfilelist{1});

% load csv data
display(csv_path);
csv_data = readtable(csv_path);
csv_data.img = num2str(csv_data.img);
csv_data.name_full = strcat(csv_data.name, '_r', csv_data.img, '.csv');


for n = 1:length(ipfilelist)
% for n = 1
    
    ippath_tmp = char(ipfilelist{n});
    [folder, baseFileName, extension] = fileparts(ippath_tmp);
    display(baseFileName);
    
    index = find(contains(csv_data.name_full, baseFileName));
    
    % load data
    M = csvread(ippath_tmp, 2);
    display(M(1:10, :));
    
    x_start = csv_data.x(index);
    y_start = csv_data.y(index);
    
    grid_stepfactor = 10;
    
    x = M(:, 1) - (x_start - padsize) * pixelsize;
    y = M(:, 2) - (y_start - padsize) * pixelsize;
    z = M(:, 3);
    
    x_grid = (0 + grid_stepfactor/2) : grid_stepfactor : ((framesize + padsize * 2) * pixelsize)
    y_grid = (0 + grid_stepfactor/2) : grid_stepfactor : ((framesize + padsize * 2) * pixelsize)
    
    [xg, yg] = meshgrid(x_grid, y_grid);
    
    
    zg = griddata(x,y,z,xg,yg,'v4');    
    % zg_2 = griddata(x,y,z,xg,yg,'linear');
    % zg = griddata(x,y,z,xg,yg,'cubic'); 
    
    oppath_tmp = char(opfilelist{n});
    csvwrite(oppath_tmp, zg);
    
    % contourf(xg,yg,zg, 20);
    
    clear M xg yg zg x t z;
    
end
