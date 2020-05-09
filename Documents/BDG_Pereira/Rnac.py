#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 21:16:48 2019

@author: lmateus
"""



from obspy.clients.fdsn import Client
from obspy.core import read
from obspy import UTCDateTime
import time 
from datetime import timedelta
import numpy as np
import  matplotlib.pyplot as plt

class ArchivoRnac():
    
    def __init__(self,miniseed):
        
        self.miniseed = miniseed
        
    def convierte(self):

        ti = time.time()
        
        #Lee un archivo .mseed con trazas de una unica estacion y varios sensores
        st1 = read('{0}'.format(self.miniseed))
        # Nos aseguramos que sea un acelerogrado HN
        st = st1.select(id="*10*")
        tr = st[0]
        
        # Extrae la metadata del miniseed 
        numero_puntos = tr.stats.npts
        duracion = tr.stats.endtime - tr.stats.starttime
        codigo_estacion = tr.stats.station
        muestreo = tr.stats.sampling_rate
        
        # Elimina respuesta instrumental y transforma en aceleraciones sin aplicar filtro
        # Para leer el inventory es necesario ingresar una fecha inicial y final, por defecto inicial 01/01/1993 y final la actual
        
        #starttime =UTCDateTime("1993-01-01T00:00:00")
        #endtime= UTCDateTime()
        
        starttime = tr.stats.starttime
        endtime = tr.stats.endtime

        # Se conecta al cliente FDSNWS de SeisComp3 y lee el inventory de la estacion relacionada en el mseed
        cliente = Client('http://10.100.100.232:8091')
        inventory = cliente.get_stations(network='CM',level="response",station=codigo_estacion,
                                         starttime=starttime, endtime=endtime)
                                         
        # Se extrae la informacion de las coordenadas del inventory
        estacion_coordenadas = inventory.get_coordinates(f"CM.{codigo_estacion}.10.HNZ",endtime)
        latitud_estacion = estacion_coordenadas["latitude"]
        longitud_estacion = estacion_coordenadas["longitude"]
        
        #pre_filt = (0.005, 0.006, 35, 40) 

        # Se convierte la traza mseed de cuentas a aceleracion 
        acel = st.remove_response(inventory=inventory, output="ACC")
        tiempo = np.arange(numero_puntos)
        #Selecciono los datos del miniseed de aceleraciones
        datosE = acel.select(component = "E")[0]
        datosN = acel.select(component = "N")[0]
        datosZ = acel.select(component = "Z")[0]
        
        # Se convierte aceleraciones a cm/s2
        EW = datosE.data * 100
        NS = datosN.data * 100
        VER = datosZ.data * 100

        # Verificamos coherencia en la longitud de los canales
        if len(EW)==len(NS)==len(VER):
            lineas = len(EW)
        else:
            print("Dimensiones de array invalidas")
            
                        
        #Crea el encabezado del archivo y la metadata de la estacion
        f = open('aceleraciones_{0}.anc'.format(codigo_estacion),'w')
        f.write('SERVICIO GEOLOGICO COLOMBIANO- RED NACIONAL DE ACELEROGRAFOS DE COLOMBIA\n')
        f.write('SISMO DE BAHIA SOLANO (CHOCO) 2017/01/12 16:06:32 MW=5.3\n')
        f.write('LATITUD DEL EVENTO(GRADOS): 5.958\n')        
        f.write('LONGITUD DEL EVENTO(GRADOS): -77.932\n')
        f.write('PROFUNDIDAD DEL EVENTO (Km): 20.5\n')
        f.write(f'CODIGO DE LA ESTACION: {codigo_estacion}\n')
        f.write(f'Estacion:{codigo_estacion} Geol:POR_IDENTIFICAR Topo:ONDULADA\n')
        f.write(f'LATITUD DE LA ESTACION (GRADOS): {latitud_estacion}\n')
        f.write(f'LONGITUD DE LA ESTACION (GRADOS): {longitud_estacion}\n')
        f.write('DISTANCIA EPICENTRAL: 65.466 km\n')
        f.write('DISTANCIA HIPOCENTRAL: 68.601 km\n')
        f.write(f'INTERVALO DE MUESTREO (SEGUNDOS): {muestreo}\n')
        f.write(f'NUMERO DE DATOS: {numero_puntos}\n')
        f.write(f'DURACION (SEGUNDOS): {duracion}\n')
        f.write('UNIDADES: cm/s^2\n')
        f.write('TIPO DE EQUIPO: EPISENSOR+Q330\n')
        f.write('ESCALA MAXIMA (G): 2\n')
        f.write('CORRECCION DE LINEA BASE: LINEA BASE NO REMOVIDA\n')
        f.write('TIPO DE DATOS: NO CORREGIDO\n')
        f.write('         EW                  VER                  NS\n')
        
        #Escribe uno a uno el dato de un array a una columnda del formato ascii
       
        
        for i in np.arange(lineas):
            
            f.write(f'    {EW[i]:11.8f}           {VER[i]:11.8f}         {NS[i]:11.8f} \n')
        
        f.close()
        
        tf = time.time()
        
        self.tiempo_rutina = timedelta(seconds=tf-ti)

        
        '''
        tiempo = np.arange(numero_puntos)
        tiempo_grafica = 0.7 * np.max(tiempo)  
        
        if np.max(EW) < abs(np.min(EW)):
            EW_max = np.min(EW)
        else:
            EW_max = np.max(EW)
            
        if np.max(NS) < abs(np.min(NS)):
            NS_max = np.min(NS)
        else:
            NS_max = np.max(NS)
            
        if np.max(VER) < abs(np.min(VER)):
            VER_max = np.min(VER)
        else:
            VER_max = np.max(VER)
        
        print("EW",EW_max,"VER",VER_max,"NS",NS_max)
        tiempo = np.arange(numero_puntos)
        plt.figure(figsize=(18,10))

        plt.subplot(311)      
        plt.plot(tiempo,EW,color="green")
        plt.ylabel("Aceleracion $cm/s^2$")
        plt.text(2.,0.2*VER_max,"EW")
        plt.text(tiempo_grafica,0.8*EW_max,(f"Aceleracion maxima ={np.round(EW_max,3)} $cm/s^2$ "),fontsize=12)
    
        plt.subplot(312)
        plt.text(2.,0.2*VER_max,"VER")
        plt.text(tiempo_grafica,0.8*VER_max,(f"Aceleracion maxima ={np.round(VER_max,3)} $cm/s^2$ "),fontsize=12)
        plt.ylabel("Aceleracion $cm/s^2$")
        
        plt.plot(tiempo,VER,color="green")
        plt.subplot(313)
        plt.ylabel("Aceleracion $cm/s^2$")
        plt.text(2.,0.2*VER_max,"NS")
        plt.text(tiempo_grafica,0.8*NS_max,(f"Aceleracion maxima ={np.round(NS_max,3)} $cm/s^2$ "),fontsize=12)      
        plt.plot(tiempo,NS,color="green")
        
        plt.xlabel("Muestra")

        plt.savefig(f"{codigo_estacion}_sinfil.png")
        plt.show()

Estaciones = ["2017-01-12-1606-38S.GUY2C_006",
              "2017-01-12-1606-16S.NOR___006",
              "2017-01-12-1606-33S.PAL___006",
              "2017-01-12-1606-53S.BET___006",
              "2017-01-12-1607-09S.FLO2__006",
              "2017-01-12-1606-13S.BAR2__004",
              "2017-01-12-1606-16S.YOT___006",
              "2017-01-12-1606-37S.PIZC__006",
              "2017-01-12-1606-55S.CRU___004",
              "2017-01-12-1607-10S.TUM___006",
              "2017-01-12-1606-16S.DBB___004",
              "2017-01-12-1606-27S.SOL___006",
              "2017-01-12-1606-46S.GARC__006",
              "2017-01-12-1606-59S.SJC___006"        
        ]

for i in (Estaciones):
    print (i)
    X = ArchivoRnac(i)
    X.convierte()
    print(X.tiempo_rutina)'''

X = ArchivoRnac("2017-01-12-1606-27S.SOL___006")
X.convierte()
print(X.tiempo_rutina)