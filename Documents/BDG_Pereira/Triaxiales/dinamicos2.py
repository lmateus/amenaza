# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 22:13:15 2020

@author: Leonardo Mateus
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import simps
from scipy.integrate import cumtrapz
import sys

class PropiedadesDinamicas():
    
    def __init__(self,path,plot):
        
        #self.ciclo = ciclo
        self.path = path
        #self.path = 'P1-M6A/'
        self.plot = plot
        self.name_file = 'Ciclos_suavizados.xlsx'
        #Leemos los datos de excel con esfuerzos ,deformaciones y tiempo
        self.data = pd.read_excel(self.path+self.name_file)
        #print(self.data)
        #esfuerzo_axial = data['esfuerzos']
        #deformacion_axial = data['deformaciones']
        tiempo = self.data['tiempo']
        
        #El numero de ciclos depende del tiempo completo del ensayo y de la frcuencia = 1 Hz, 100 mediciones por ciclo
        tiempo_total = int(len(tiempo)/100)
        print(tiempo_total)
        self.informacion_ciclos = []
        
        #Calcula un arreglo con las mediciones en donde empiezan y terminan los ciclos
        for i in range(tiempo_total):
            numero_ciclo = i
            ciclo_inicio = numero_ciclo * 100
            ciclo_fin = ciclo_inicio +101
            self.informacion_ciclos.append([numero_ciclo,ciclo_inicio,ciclo_fin])
    
    def filtra_ciclos(self,ciclo):
        self.ciclo = ciclo
        #Extrae la informacion por cada ciclo
        self.filtro = self.data[self.informacion_ciclos[self.ciclo][1]:self.informacion_ciclos[self.ciclo][2]]
        #Extraemos las columas esfuerzos y deformaciones y dividimos por 100
        esfuerzo = self.filtro['esfuerzos']
        deformacion = self.filtro['deformaciones']/100

        #Determinamos el esfuerzo y deformacion promedio
        promedio_esfuerzo = (esfuerzo.max() + esfuerzo.min())/2
        promedio_deformacion = (deformacion.max() + deformacion.min())/2
        
        #Centramos el ciclo para dejar el promedio en el centro (0,0)
        esfuerzo_centrado = esfuerzo - promedio_esfuerzo
        deformacion_centrada = deformacion - promedio_deformacion
        
        #Calculamos los valores extremos del ciclo centrado
        esfuerzo_maximo2 = esfuerzo_centrado.max()
        esfuerzo_minimo2 = esfuerzo_centrado.min()
        deformacion_maxima2 = deformacion_centrada.max()
        deformacion_minima2 = deformacion_centrada.min()
        
        def_angular = deformacion_maxima2 *1.5
        #Creamos un arreglo para mostrar la linea del modulo E Secante
        arreglo_esfuerzo2 = [esfuerzo_centrado.min(),esfuerzo_centrado.max()]
        arreglo_deformacion2 = [deformacion_centrada.min(),deformacion_centrada.max()]
        
        promedio_esfuerzo2 = (esfuerzo_centrado.max() + esfuerzo_centrado.min())/2
        promedio_deformacion2 = (deformacion_centrada.max() + deformacion_centrada.min())/2
        
        E_secante2 = (esfuerzo_centrado.max()-esfuerzo_centrado.min()) / (deformacion_centrada.max()-deformacion_centrada.min())
        G_secante = E_secante2/3
        
        if self.plot == True:
            plt.figure(figsize=(12,6))
            plt.title(f'Ciclo {ciclo}')
            plt.plot(deformacion,esfuerzo,'--',label='Sin Corregir')
            plt.plot(deformacion_centrada,esfuerzo_centrado,label='Centrada')
            plt.plot(arreglo_deformacion2,arreglo_esfuerzo2,label='E secante',color='red')
            plt.xlabel('$\epsilon_a$ Deformacion axial')
            plt.ylabel('$\sigma_d$ Esfuerzo desviador [kN] ')
            plt.legend()
            plt.grid()
            plt.show()
            #plt.savefig(f'./CarpetaPlot/centrado{self.ciclo}')
  
        esfuerzo_amortiguamiento = esfuerzo_centrado + esfuerzo_maximo2
        deformacion_amortiguamiento = deformacion_centrada + deformacion_maxima2
        
        deformacion_amortiguamiento_max = deformacion_amortiguamiento.max()
        deformacion_amortiguamiento_min = deformacion_amortiguamiento.min()
        
        #print(deformacion_amortiguamiento_min)
        
        ind_def_max = np.where(deformacion_amortiguamiento==deformacion_amortiguamiento_max)[0]
        ind_def_min = np.where(deformacion_amortiguamiento==deformacion_amortiguamiento_min)[0]
        
        ind_def_max = int(ind_def_max[0])
        ind_def_min = int(ind_def_min[0])
        
        '''I1 = simps(esfuerzo_amortiguamiento[0:ind_def_max+1],deformacion_amortiguamiento[0:ind_def_max+1])
        I2 = simps(esfuerzo_amortiguamiento[ind_def_min:101],deformacion_amortiguamiento[ind_def_min:101])
        I3 = simps(esfuerzo_amortiguamiento[ind_def_max:ind_def_min+1],deformacion_amortiguamiento[ind_def_max:ind_def_min+1])
        print(self.ciclo)'''
        
        I1_1 = cumtrapz(esfuerzo_amortiguamiento[0:ind_def_max+1],deformacion_amortiguamiento[0:ind_def_max+1])[-1]
        I2_1 = cumtrapz(esfuerzo_amortiguamiento[ind_def_min:101],deformacion_amortiguamiento[ind_def_min:101])[-1]
        I3_1 = cumtrapz(esfuerzo_amortiguamiento[ind_def_max:ind_def_min+1],deformacion_amortiguamiento[ind_def_max:ind_def_min+1])[-1]
        A_LoopT = I1_1+I2_1+I3_1
        #print('amortiguamiento T',amortiguamintoT)
        #A_Loop = (I1+I2+I3)
        
        if self.plot == True:

            plt.figure(figsize=(12,6))
            plt.title(f'Area interna del ciclo {ciclo}')
            plt.plot(deformacion_amortiguamiento[0:ind_def_max+1],esfuerzo_amortiguamiento[0:ind_def_max+1],color='red')
            plt.plot(deformacion_amortiguamiento[ind_def_min:101],esfuerzo_amortiguamiento[ind_def_min:101],color='green')
            plt.plot(deformacion_amortiguamiento[ind_def_max:ind_def_min+1],esfuerzo_amortiguamiento[ind_def_max:ind_def_min+1],color='blue')
            plt.fill_between(deformacion_amortiguamiento[0:ind_def_max+1],esfuerzo_amortiguamiento[0:ind_def_max+1],0,alpha=0.7,color='red')
            plt.fill_between(deformacion_amortiguamiento[ind_def_min:101],esfuerzo_amortiguamiento[ind_def_min:101],0,color='green',alpha=0.7)
            plt.fill_between(deformacion_amortiguamiento[ind_def_max:ind_def_min+1],esfuerzo_amortiguamiento[ind_def_max:ind_def_min+1],0,color='yellow',alpha=0.7)
            plt.xlabel('$\epsilon_a$ Deformacion axial')
            plt.ylabel('$\sigma_d$ Esfuerzo desviador [kN] ')
            plt.grid()
            plt.plot()
            plt.show()
            #plt.savefig(f'./CarpetaPlot/{self.ciclo}')
        
        A_triangulo = deformacion_maxima2 * esfuerzo_maximo2/2
        
        constante = 1/(2*3.14159)
        constante2 = 1 / (4*3.14159)
        
        #variable = (A_Loop /(G_secante*def_angular**2))
                
        #D = constante * variable
        #D2 = constante2*(A_Loop/A_triangulo)
        
        self.amortiguamientoT = constante2*(A_LoopT/A_triangulo)

        self.G_secante = G_secante
        #self.amortiguamiento = D2
        self.def_angular = def_angular
        print('G=',G_secante,'amortiguamiento2',self.amortiguamientoT,'AmortiT',self.amortiguamientoT)

path = sys.argv[1]
ciclo_inicio = int(sys.argv[2])
ciclo_fin = int(sys.argv[3])
plot = bool(int(sys.argv[4]))

defor_angular = []
amortiguamiento = []
amortiguamientoT2 = []
moduloG = []
X = PropiedadesDinamicas(path,plot)
for i in range(ciclo_inicio,ciclo_fin,1):
    try:
        X.filtra_ciclos(i)
        defor_angular.append(X.def_angular)
        #amortiguamiento.append(X.amortiguamiento)
        amortiguamientoT2.append(X.amortiguamientoT)
        moduloG.append(X.G_secante)
    except:
        print('error de dimension')
        #defor_angular.append(np.nan)
        
        #amortiguamientoT2.append(np.nan)
        #moduloG.append(np.nan)
#print(defor_angular,amortiguamiento)

plt.figure()
#plt.plot(defor_angular,amortiguamiento,'o')
plt.plot(defor_angular,amortiguamientoT2,'o')
plt.plot()
plt.grid()
plt.xlabel('Deformacion angular $\gamma$')
plt.ylabel('Amortiguamiento D')
#plt.ylim(0,0.1)
plt.show()

plt.figure()
plt.plot(defor_angular,moduloG,'o')
plt.plot()
plt.grid()
plt.xlabel('Deformacion angular $\gamma$')
plt.ylabel('Modulo de Corte G')
plt.show()

ColumnaD = pd.DataFrame(zip(amortiguamientoT2,amortiguamientoT2),columns=['AmortiguamientoTrapecio','amortiguamientoTrapecio'])
ColumnaD.to_excel(X.path+f"D_{X.path.split('/')[0]}_LM.xlsx")