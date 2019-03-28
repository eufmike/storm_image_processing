%% Define the path of folders
close all;
folder_path = '/Volumes/LaCie_DataStorage/xiaochao_wei_STORM imaging/STORM_imaging/';
analysis_dir = 'analysis_20190308';
st_dir = 'spacial_test';
ip_dir = 'spacialdata_local'; % specify the input folder
op_dir = 'spacialdata_local_int';
% output_folder = 'raw_test_output'; % specify the output folder

% create path
ip_path = fullfile(folder_path, analysis_dir, st_dir, ip_dir);
op_path = fullfile(folder_path, analysis_dir, st_dir, op_dir);

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


%for n = 1:length(ipfilelist)
for n = 1
    ippath_tmp = char(ipfilelist{n});
    
    M = csvread(ippath_tmp, 2);
    
    display(M(1:10, :));
    x = M(:, 1);
    y = M(:, 2);
    z = M(:, 3);
    [xg, yg] = meshgrid(10 : 20 : 20480);
    zg = griddata(x,y,z,xg,yg,'v4');    
    % zg_2 = griddata(x,y,z,xg,yg,'linear');
    
    oppath_tmp = char(opfilelist{n});
    csvwrite(oppath_tmp, zg);
    
    contourf(xg,yg,zg, 20);
    
    % clear M xg yg zg x t z;
end

