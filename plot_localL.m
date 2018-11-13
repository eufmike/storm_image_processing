%% Define the path of folders
close all;
folder_path = '/Volumes/LaCie_DataStorage/xiaochao_wei_STORM imaging/STORM_imaging/analysis/spacial_test/';
input_folder = 'datalocalL_test'; % specify the input folder
output_folder = 'datalocalL_interpolation';
% output_folder = 'raw_test_output'; % specify the output folder

input = dir(fullfile(folder_path, input_folder));
filenames = {input.name};

regexp_crit = '^[^.]+'; % the pattern of general expression
rxResult = regexp(filenames, regexp_crit); % pick the string follow the rule
nodot = (cellfun('isempty', rxResult)==0); % convert to logicals
filenames_nodot = filenames(nodot);

display(filenames_nodot);

for n = 1:length(filenames_nodot)
    filename = filenames_nodot(n);
    inputfiledir = char(fullfile(folder_path, input_folder, filename));   
    
    M = csvread(inputfiledir, 2);
    
    display(M(1:10, :));
    x = M(:, 1);
    y = M(:, 2);
    z = M(:, 3);
    [xg, yg] = meshgrid(0 : 20 : 20480);
    zg = griddata(x,y,z,xg,yg,'v4');
    
    outputfiledir = char(fullfile(folder_path, output_folder, filename));
    csvwrite(outputfiledir, zg);
    
    % contourf(xg,yg,zg, 20);
    
    clear M xg zg x t z;
end

