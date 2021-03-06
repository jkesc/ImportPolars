%Written by Jan-Karl L. Escher 08.09.21

%% This is a demonstration of how the importPolars function can be used.

dataLib=importPolars('S826_Ashes17.txt'); %Imports the data from your file. 
%REMEMBER TO CHANGE THIS NAME TO A FILE WHICH IS ACTUALLY A POLAR FILE IN YOUR DIRECTORY

%If you prefer to choose the polar files from an explorer, you can
%comment out the first dataLib-line, and instead uncomment the following
%one.
%dataLib=importPolars(uigetfile('*.txt'));

keys= dataLib.keys; %keys now contains the Reynolds numbers from the file

%the individual keys can be extracted by using indexing in curly braces:
firstKey=keys{1};
fprintf('\nThis is the value of firstKey: %s\n',firstKey)

%Note that the keys are strings, not numbers. To transform a string 
%into a number, you can use the string2double function:
firstKeyValue=str2double(firstKey);

%This value can now be used to compare to the Re number you find in your
%algorithm. When you have decided on which polar file you want to use, you
%use the key (as a string) to extract all of the polar data for this Re:

FirstPolarData=dataLib(firstKey);

%Now the FirstPolarData variable is a matrix, which contains four columns,
%with alpha, Cl, Cd and Cm respectively. You only need the first three
%columns.

%Play around a bit with the new variables that you see in your workspace,
%to familiarize yourself with them.

%If you want to import multiple files from airfoiltools, you first have to download
%the files individually, and then run the function 'mergeAirfoiltools('polarName.txt')'
%then you can run importPolars('polarName.txt') the same way as for ashes
%files.

