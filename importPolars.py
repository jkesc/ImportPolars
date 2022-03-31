# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 14:59:10 2022

@author: jkescher
"""


def importAshesPolars(filename, source):
    # Import all of the relevant python modules
    import os
    import numpy as np
    import pandas as pd
    from scipy.interpolate import LinearNDInterpolator
    from scipy.interpolate import interp1d
    if source == 'Ashes':
        # Open the file and read all of its lines.
        with open(filename, "r") as bladefile:
            bladelines = bladefile.readlines()
        # Set initial values for the Re and the number of files to skip in the
        # header (Lines which are not commented out by an !, that is).
        ReStr = "Nan"
        skiplines = 4
        # create a temporary file, to be able to make a csv from our data later
        # The temporary file is supposed to contain five columns: Re, AoA, Cl,
        # Cd and Cm. Not that Cm is never used in this course.
        with open("temp.txt", "w") as tempTxt:

            # Iterate through all lines:
            for line in bladelines:
                # If the line is not commented out:
                if not (line[0] == "!"):

                    # If it is the line describing the Reynolds number,
                    # we remember the new Re value
                    # and know that we have to skip the next three lines.
                    if line[14:16] == "Re":
                        ReStr = line[1:11]
                        skiplines = 3
                    # If it's one of the three lines after Re, we skip it.
                    elif not (skiplines == 0):
                        skiplines -= 1
                    # Else, write the lift, AoA and cm to the temporary
                    # text file.
                    else:
                        tempTxt.write(ReStr+line)
        # now we interpret the txt as a comma separated values (csv) file, but
        # separated with whitespaces instead of commas.
        # We know what the columns are supposed to represent:
        colNames = ['Re', 'AoA', 'Cl', 'Cd', 'Cm']
        ClCdFrame = pd.read_csv("temp.txt", delim_whitespace=True,
                                names=colNames)

        # Multiply the Re by 10^6, as Ashes gives Re in million
        ReList = np.asarray(ClCdFrame["Re"]).astype(float)*1e6
        AoAList = np.asarray(ClCdFrame["AoA"]).astype(float)
        ClList = np.asarray(ClCdFrame["Cl"]).astype(float)
        CdList = np.asarray(ClCdFrame["Cd"]).astype(float)
    # If the files are imported from airfoiltools, there is one file for each
    # Re-value. We will iterate through all of these, and extract data.
    elif source == 'Airfoiltools':
        # initialize all of the arrays
        ReList = np.array([])
        AoAList = np.array([])
        ClList = np.array([])
        CdList = np.array([])
        # two allowed cases: either all of the files to be imported are
        # Specified as lists, in that case the entire filename must be
        # specified, or only the filename without the reynolds number is given.
        # in that case, the program iterates through the current folder, to
        # find all .txt files starting with the same name.
        if type(filename) == list:
            file_iterator = filename
        elif type(filename) == str:
            file_iterator = []
            for file in os.listdir():
                if file.startswith(filename) and file.endswith('.txt'):
                    file_iterator.append(file)
        # Then we iterate through all the files:
        for file in file_iterator:
            lineCount = 0
            with open(file, 'r') as bladeFile:
                lines = bladeFile.readlines()
                for line in lines:
                    # we know on which line the Reynolds number is given:
                    if lineCount == 8:
                        Re = float(''.join(line.split()[5:8]))
                    # and on which line the actual blade data starts:
                    elif lineCount > 11:
                        # all of this is then saved in the lists.
                        ReList = np.append(ReList, Re)
                        AoA, Cl, Cd = line.split()[0:3]
                        AoAList = np.append(AoAList, float(AoA))
                        ClList = np.append(ClList, float(Cl))
                        CdList = np.append(CdList, float(Cd))
                    lineCount += 1
    # Create a list of points with the Parameters, Re and AoA
    points = [(x, y) for (x, y) in zip(ReList, AoAList)]

    # Return functions for the lift and drag at different Re and different AoA
    Clfun = LinearNDInterpolator(points, ClList)
    Cdfun = LinearNDInterpolator(points, CdList)

    # In order to get the optimal angle of attack, we'll have to
    # do some more.
    Aoa = []
    Re = []
    RateOld = -1
    first = True
    # Entering a for loop, iterating through all the points.
    for (i, j) in points:
        # For the first iteration, we'll have to remember the first Re
        if first is True:
            ReOld = i
            first = False
            # If the next iteration has the same Re as the last iteration, we
            # check the Lift-drag ratio and keep this AoA if it's better than
            # the last best rate
        if i == ReOld:
            rate = Clfun(i, j)/Cdfun(i, j)
            if rate > RateOld:
                Aoa_current = j
                RateOld = rate
                # Otherwise save the Reynolds number together
                # with the best AoA and update ReOld.
        else:
            Re.append(ReOld)
            ReOld = i
            Aoa.append(Aoa_current)
            RateOld = Clfun(i, j)/Cdfun(i, j)
            # Save all of those values at the end of the loop.
    Re.append(ReOld)
    Aoa.append(Aoa_current)
    AoaMaxFun = interp1d(Re, Aoa)

    # And the limits for the reynolds number (upper and lower)
    Relims = [np.min(ReList), np.max(ReList)]

    return [Clfun, Cdfun, Relims, AoaMaxFun]
