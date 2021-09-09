function filename = mergeAirfoiltools(filename)
% This function concatenates multiple txt files. In this case for use in
% importing airfoil polars from airfoiltools.com, but can be used in other
% settings as well.
%It returns the name of the file which the merged files were saved to.
%% Checking if the filename is in the right format, and opening it for writing purposes
    if nargin<1
        filename='airfoiltools.txt';
    elseif convertCharsToStrings(filename(end-3:end)) ~= ".txt"
        filename=strcat(filename,'.txt');
    end
    %% Opening the files to be merged and merging them
    [readFileNames, readFilePaths]=uigetfile('*.txt','Multiselect','on','Please select the files you want to merge (Hold Ctrl to mark multiple files)');
    try
        fidW=fopen(filename,'w');
        for i=readFileNames,j=readFilePaths;
            fidR=fopen(strcat(j,i{1}),'r');
            line=fgetl(fidR);
            while ischar(line)
                fprintf(fidW,'%s\n',line);
                line=fgetl(fidR);
            end
            fclose(fidR);
        end
        fclose(fidW);
    catch Err
        fclose('all');
        error('Failed to read all files')
    end
    
end
