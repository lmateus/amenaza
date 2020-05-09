# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 11:24:27 2020

@author: Leonardo Mateus
"""

import matplotlib.pyplot as plt 
import matplotlib.animation as animation
import numpy as np
import pandas as pd
import sys

path = sys.argv[1]
nivel_def = sys.argv[2]

#Lee el archivo .log de los triaxiales
#path = 'P1-M26/'
name_file = nivel_def +' - Cyclic Shear.log'
file_name = path + name_file
#Lee un archivo y lo transforma en un DataFrame
file = pd.read_csv(file_name,sep='\t',header=1)
file = file.drop(0,axis=0)

#Lee las columnas del dataframe
load = file['Load'].astype(float)
actuator = file['Actuator'].astype(float)
sigma_a = file['Load'].astype(float)
sigma_c = file['Cell Pressure'].astype(float)
presion_poros = file['Pore Pressure'].astype(float)
inc_presion_poros = presion_poros - presion_poros[1]
p = (sigma_a + 2*sigma_c)/3
q = sigma_c - sigma_a 

p_efectivo = p - inc_presion_poros


#data = np.loadtxt("example.txt", delimiter=",")
x = actuator
y = load

fig = plt.figure()
ax = fig.add_subplot(111)
plt.grid()
plt.xlabel('Actuator (mm)')
plt.ylabel('Load [kN]')
plt.title(file_name)
line, = ax.plot([],[], 'c',color='red')
line2, = ax.plot([],[],'--')
ax.set_xlim(1.1*np.min(x), 1.1*np.max(x))
ax.set_ylim(1.1*np.min(y),1.1* np.max(y))


def animate(i,factor):
    line.set_xdata(x[:i])
    line.set_ydata(y[:i])
    line2.set_xdata(x[:i])
    line2.set_ydata(y[:i])

    return line,line2

K = 0.75 # any factor 
ani = animation.FuncAnimation(fig, animate, frames=len(x), fargs=(K,),
                              interval=100, blit=True)
plt.show()