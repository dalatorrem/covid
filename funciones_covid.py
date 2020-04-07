# -*- coding: utf-8 -*-
"""Untitled7.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1MpRwtYQJb3TeVuTk2JK1INjSj0dX98Cg
"""

import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt


#####################################################################
#### Función para visualizar
#####################################################################
def visualizar():
  # trayendo los datos de la página de la UE y creando dataframe
  wget -O casedistribution.csv https://opendata.ecdc.europa.eu/covid19/casedistribution/csv
  datos = pd.read_csv("casedistribution.csv")[['dateRep','cases','deaths','countriesAndTerritories']]
  paises=datos['countriesAndTerritories'].value_counts().index.array
  datos_cum=crear_data_frame(datos)
  paises_mayor_1000_data,paises_mayor_1000=hacer_boxplot(datos_cum,paises)
  print('En el siguiente gráfico se han agrupado los países con más de mil casos, tenga en cuenta las escalas')
  datos_cum=hacer_graficos_por_paises(paises_mayor_1000_data,paises_mayor_1000,datos_cum)




### funciones

#####################################################################
# función para crear data frame con sumas cumulativas
#####################################################################
def crear_data_frame(datos,paises):
  cum=0
  for pais in paises:
    pais_datos=datos[datos['countriesAndTerritories']==pais]
    pais_datos=pais_datos.iloc[ ::-1]
    pais_datos['cum_cases']=pais_datos['cases'].cumsum()
    pais_datos['cum_deaths']=pais_datos['deaths'].cumsum()
    if cum==0:
      datos_cum=pais_datos
      cum=1
    else:
      datos_cum=pd.concat([datos_cum,pais_datos])
  return datos_cum
#####################################################################
# función para graficar un boxplot del número de casos de países 
# con más de 1000 infectados 
#####################################################################

def hacer_boxplot(datos_cum,paises):
  division = pd.DataFrame({'countriesAndTerritories':[], 'cum_cases':[]})
  for pais in paises:
    cum=datos_cum[datos_cum['countriesAndTerritories']==pais]
    cum=cum['cum_cases'].iloc[-1]
    dato=pd.DataFrame([[pais,cum]],columns=['countriesAndTerritories','cum_cases'])
    division=pd.concat([division, dato])
  paises_mayor_1000_data=division[division['cum_cases']>1000]
  paises_mayor_1000_data=paises_mayor_1000_data.sort_values(by='cum_cases')
  paises_mayor_1000=paises_mayor_1000_data['countriesAndTerritories']
  red_square = dict(markerfacecolor='r', marker='s')
  print('Si desea ver el boxplot del Número total de casos por países escriba "SI" (en mayúsculas)')
  boxplot_pregunta=input()
  if boxplot_pregunta=='SI':
    fig, ax = plt.subplots(figsize=(15,1))
    ax.set_title('Países con más de 1000 casos reportados')
    ax.boxplot(paises_mayor_1000_data['cum_cases'], vert=False, flierprops=red_square)
    ax.set_yticklabels('')
    ax.set_xlabel('Número de casos')
    plt.show()
  print('Si desea ver la tabla del total de casos por países escriba "SI" (en mayúsculas) ')
  tabla=input()
  if tabla=='SI':
    paises_mayor_1000_data
  return paises_mayor_1000_data,paises_mayor_1000

def hacer_graficos_por_paises(paises_mayor_1000_data,paises_mayor_1000,datos_cum):
  no_graficos=len(paises_mayor_1000)//5+1
  no_filas=math.ceil(no_graficos//3)
  fig,axes=plt.subplots(nrows=no_filas,ncols=3,figsize=(19,3.5*no_filas))
  eje_x=datos_cum[datos_cum['countriesAndTerritories']=='China']
  eje_x['dia']=np.arange(0,len(eje_x['cum_cases']))
  dia_num=lambda data,dia:data.loc[data['dateRep']==dia,'dia'].iloc[0]
  datos_cum['dia']=[dia_num(eje_x,dia) for dia in datos_cum['dateRep']]
  print('Curvas de casos para todos los países con más de mil casos')
  print( 'El día 0 corresponde al 31 de diciembre de 2019')
  print('Introduzca el día inicial, por ejemplo 0')
  dia_inicial=int(input())
  maximo=len(eje_x['dia'])-1
  print('Introduzca el último día para la gráfica, valor máximo',maximo)
  dia_final=int(input())
  arreglo_x=np.arange(dia_inicial,dia_final)
  datos=pd.DataFrame(columns=datos_cum.columns)
  grupo=1
  for fil in range(no_filas):
    for col in range(3):
      ind_p_min=(3*fil+col)*5
      ind_p_max=min(ind_p_min+5,len(paises_mayor_1000))
      if ind_p_min<len(paises_mayor_1000):
        paises_cum_hoy=paises_mayor_1000_data.iloc[ind_p_min:ind_p_max]
        y_limite=paises_cum_hoy['cum_cases'].iloc[-1]
        axes[fil,col].set_xlim(left=dia_inicial,right=dia_final)
        axes[fil,col].set_ylim(bottom=-0.1*y_limite,top=1.1*y_limite)
        for i in range(0,len(paises_cum_hoy)):
          datos_c=datos_cum[datos_cum['countriesAndTerritories'] == paises_cum_hoy['countriesAndTerritories'].iloc[i]]
          axes[fil,col].plot(datos_c['dia'],datos_c['cum_cases'])
          datos=pd.concat([datos,datos_c])
        axes[fil,col].legend(paises_cum_hoy['countriesAndTerritories'])
        axes[fil,col].set_xlabel('Número de días')
        axes[fil,col].set_ylabel('Número de casos',)
        grupo_s=str(grupo)
        grupo=grupo+1
        axes[fil,col].set_title('Grupo'+grupo_s)
  plt.show()
  return datos_cum
