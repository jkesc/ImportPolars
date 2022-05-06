# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 11:32:40 2022

@author: jkescher
"""

if __name__ == '__main__':
    # importing importPolars as a module
    import importPolars as ip
    # and some modules to visualize the data
    import numpy as np
    import matplotlib.pyplot as plt
    # the three lines below give each of the three cases. uncomment the one you want to try, to test it.
    # Remember that you will have to change the name between ashes and airfoiltools if the file format changes as well
    filename = 'airfoiltools xf-a18-il-'
    # filename = ['airfoiltools xf-a18-il-50000.txt','airfoiltools xf-a18-il-100000.txt']
    # filename='s826_Ashes17.txt'
    ClFun, CdFun, AoAmax, Relims, AoALims = ip.importPolars(filename,
                                                            'airfoiltools')
                                                            # 'ashes')
    aoa_choose=np.mean(AoALims)
    re_choose=np.mean(Relims)
    cl_choose=ClFun(re_choose,aoa_choose)
    print(f'Cl at an angle of attack of {aoa_choose} and Reynolds number of {re_choose} is: Cl = {cl_choose}')
    Aoa=np.linspace(min(AoALims), max(AoALims))
    Re_range = np.linspace(min(Relims),max(Relims),10)
    for Re in Re_range:
        plt.figure(1)
        plt.plot(Aoa, ClFun(Re,Aoa))
        plt.title('Lift vs angle of attack for the range')
        plt.xlabel('AoA[deg]')
        plt.ylabel('Cl [-]')

        plt.figure(2)
        plt.plot(Aoa, CdFun(Re,Aoa))
        plt.title('Drag vs angle of attack')
        plt.xlabel('AoA[deg]')
        plt.ylabel('Cd [-]')

    plt.figure(3)
    plt.plot(Re_range,AoAmax(Re_range))
    plt.title('Best lift to drag ratio for the range of reynolds numbers')
    plt.ylabel('AoA [deg]')
    plt.xlabel('Re [-]')
    plt.show()
