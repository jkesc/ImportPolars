function dataLib = importPolars(filename,version)
%This function was written by Jan-Karl L. Escher for use in the course
%"Design of a wind turbine" at NTNU.
%Last Revised on 09.09.21

%%%% Explanation
%the filename is the name of the ashes polar file you want to load.
%version is the name of the version of ashes the polar file was created
%with. The two valid options here are '16' and '17' for ashes version 3.16
%and 3.17. If no version is specified, the function will try to deduce the
%version on its own.

%This function will take in the name of a polar file on .txt form as output
%by ASHES, and outputs this in the form of a Map, readable by matlab.

%A map is a data structure which uses keywords to find related data. In
%this case the keywords will correspond to the Reynolds number of the polar
%data.

%For a demo of what this function does, please run the file
%"ImportPolarsDemo.m".
%% Reading in the file and guessing a version if nothing is specified by the operator
[standardName,standardVersion]=standardizeFile(filename);

if nargin ==1
    version = standardVersion;
end
%% reading in data to the map, based on the version type
dataLib=containers.Map('KeyType','char','ValueType','any');
switch version
    %% if it's ashes 3.16, we can read in data based on the specified number of lines per polar
    case '16'
        dataMat=readmatrix(standardName);
        dataMat=dataMat(4:end,1:4);
        endpoint=max(size(dataMat)); %Find where I should iterate to
        i=find(~isnan(dataMat(:,1)),1,'first');
        
        while i<= endpoint
            Re=dataMat(i,1);
            i=i+3;
            elementNo=dataMat(i,1);
            i=i+1;
            elements=dataMat(i:i+elementNo-1,:);
            dataLib(strcat(num2str(Re),'e+06'))=elements;
            i=i+elementNo;
        end
        %% If it is version 17, we have to read in all the lines and save the data while doing this.
    case '17'
        try
            %% opening the file 
            fid=fopen(standardName,'r');
            line=fgetl(fid);
            tokens=split(line);
            Re=tokens{2};
            elements=[];
            line=fgetl(fid);
            
            %% Reading through entire file and saving values
            while ischar(line)
                tokens=split(line);
                if convertCharsToStrings(tokens{3})=="Re"
                    dataLib(strcat(num2str(Re),'e+06'))=elements;
                    elements=[];
                    Re=tokens{2};
                else
                    elements=[elements;str2double(tokens{2}) str2double(tokens{3}) str2double(tokens{4}) str2double(tokens{5})];
                end
                line=fgetl(fid);
            end
            dataLib(strcat(num2str(Re),'e+06'))=elements;
            %% Closing the files, regardless of if there was an error or not.
            fclose(fid);
        catch
            fclose('all');
            error('There was an error in importPolars.m, in case 17')
        end
end
end

function [outputname,version] = standardizeFile(filename,outputname)
%Function to make all polar files from ashes on the same format with
%relevant data for the project
if nargin==1
    outputname='temp.txt';
end
%Using try-catch in order to close the file if anything goes wrong.
try
    %Reading in the file
    fid_r=fopen(filename,'r');
    fid_w=fopen(outputname,'w');
    line=fgetl(fid_r);
    
    %trying to guess the file based on the format
    versionCheckSplit=split(line);
    versionCheckTok=convertCharsToStrings(versionCheckSplit{2});
    switch versionCheckTok
        case "Name:"
            version = "17";
        case "------------"
            version="16";
        otherwise
            warning('No matching case found. version sat to 17')
            version="17";
            %If there was no match, we assume the latest version of ashes
    end
            %remove all unimportant parts of the file.
            while ischar(line)
                if line(1) ~= '!'
                    fprintf(fid_w,strcat(line,'\n'));
                end
                line=fgetl(fid_r);
            end
catch
    error('An error occured in standardizeFile\n')
end
fclose('all');
end