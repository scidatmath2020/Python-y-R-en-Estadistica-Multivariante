# -*- coding: utf-8 -*-
"""
Created on Sun Nov 22 17:48:08 2020

@author: hp
"""

import numpy as np
import scipy as sc
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

from math import pi
from pandas.plotting import scatter_matrix
from pandas.plotting import andrews_curves

#%%


cancer = pd.read_csv("C:/Users/hp master/Documents/SciData/Est_Mult/Mod01. Espacios multivariantes/C01. Mediciones con multiples variables/cancer.csv",index_col="id")
cancer.head()

#%%

'''¿Cuántos individuos tienen cáncer maligno y cuántos no?

Mostrar esta información gráficamente.'''

cancer["diagnosis"].value_counts()

#%%

sns.countplot("diagnosis",data=cancer)
plt.show()

#%%

cancer["diagnosis"] = cancer["diagnosis"].astype("category")
cancer.info()

#%%

'''Observamos que las variable 32 no nos sirve. Procedemos a eliminarla:'''

cancer.drop("Unnamed: 32",axis=1,inplace=True)
cancer.info()


#%%

'''¿Hay valores nulos?'''

print("Hay valores nulos?\n",cancer.isnull().values.any())


#%%

##########
##########  BOXPLOTS
##########


plt.figure(figsize=(20,20)) #controla el tamaño del gráfico
sns.boxplot(data = cancer)
plt.xticks(rotation=90) #controla la rotación de las etiquetas en el eje X
plt.show()


#%%

'''Como se puede observar, hay muchos valores atípicos que dificultan la lectura de la gráfica. 
Estandaricemos cada característica para obtener una mejor visualización.'''

#crea una nueva tabla, cancer_estandarizado, que no contiene diagnosis
cancer_numerico = cancer[cancer.columns[1:]] 

cancer_numerico.head()

#pip install sklearn

from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
caracteristicas_escaladas = scaler.fit_transform(cancer_numerico.values)
cancer_estandarizado = pd.DataFrame(caracteristicas_escaladas,
                                       index = cancer_numerico.index,
                                       columns=cancer_numerico.columns)
cancer_estandarizado

#%%

plt.figure(figsize=(14,8)) #controla el tamaño del gráfico
sns.boxplot(data = cancer_estandarizado)
plt.xticks(rotation=90) #controla la rotación de las etiquetas en el eje X
plt.show()

#%%

'''Un enfoque estadístico robusto habría considerado valores atípicos a todos los valores 
que superan 3 (o 2.5) en el eje Y. sin embargo, dado el rango limitado de distribución de datos 
(de aproximadamente -2.5 a aproximadamente +11) y la disponibilidad de datos que no es muy alta 
(solo 569 observaciones), se podría utilizar un enfoque "visual" para la detección de los valores 
atípicos (basado en densidad de los puntos por encima de un umbral específico). 

Por ejemplo, eliminar las observaciones que superan el valor 6.

Los valores atípicos podrían ser indicativos de datos incorrectos, procedimientos erróneos o áreas 
experimentales donde algunas teorías pueden no ser válidas. Antes de eliminarlos, deberíamos 
discutir con expertos en este dominio para entender por qué estos datos no son válidos 
(por ejemplo, el equipo de medición falló, el método de medición fue poco confiable por alguna razón,
había contaminantes, etc).'''


#Eliminar atípicos

cancer_limpio=cancer_estandarizado[cancer_estandarizado.apply(lambda x: np.abs(x - x.mean()) / x.std() < 6).all(axis=1)]
cancer_limpio.shape

cancer_limpio["Id"] = cancer_limpio.index
cancer["Id"] = cancer.index


cancer_limpio.info()
cancer.info()

plt.figure(figsize=(14,8))
sns.boxplot( data = cancer_limpio[cancer_limpio.columns[:30]])
plt.xticks(rotation=90)  
plt.show()

#%%

#########
#########  BOXPLOT PARA CADA CADA VARIABLE DIVIDIDO POR ESPECIE DE CÁNCER
#########


cancer[["Id","diagnosis"]]

cancer_limpio_diagnostico = cancer_limpio.join(cancer[["Id","diagnosis"]].set_index(["Id"]),
                                               on=["Id"],
                                               how="inner")
cancer_limpio_diagnostico.head()

cancer_limpio_diagnostico.drop("Id",axis=1,inplace = True)
cancer_limpio_diagnostico.info()

plt.figure(figsize=(14,8))
cancer_limpio_diagnostico.boxplot(by="diagnosis",figsize=(24,12))
plt.xticks(rotation=90)
plt.show()

cancer_limpio_diagnostico.shape

#%%

'''Convertimos la variable diagnostico a una representación numérica'''

cancer["diagnosis"] = cancer["diagnosis"].map({"M":1,"B":0})
cancer["diagnosis"].value_counts()

#%%

'''Dividimos la tabla en tres tablas dependiendo del tipo de medida de las características.'''

caracteristicas_media = list(cancer.columns[1:11])
caracteristicas_sd = list(cancer.columns[11:21])
caracteristicas_max = list(cancer.columns[21:31])

print(caracteristicas_media, "\n",caracteristicas_sd,"\n",caracteristicas_max)

#%%

from pandas.plotting import scatter_matrix


colores = {0:"blue",1:"red"}
colors = cancer["diagnosis"].map(lambda x: colores.get(x))

sm = scatter_matrix(cancer[caracteristicas_media],c=colors,alpha=0.5,figsize=(15,15))

#Orientación de los letreros

[s.xaxis.label.set_rotation(45) for s in sm.reshape(-1)]
[s.yaxis.label.set_rotation(0) for s in sm.reshape(-1)]
[s.get_yaxis().set_label_coords(-0.9,0.5) for s in sm.reshape(-1)]
[s.set_xticks(()) for s in sm.reshape(-1)]
[s.set_yticks(()) for s in sm.reshape(-1)]


plt.show()

#%%

caracteristicas_media.append("diagnosis")
sns.pairplot(cancer[caracteristicas_media],hue="diagnosis",height=1.5)
plt.show()

caracteristicas_media = caracteristicas_media[:10]


#%%

############
############ COVARIANZAS Y CORRELACIONES
############


cov_matrix = cancer_numerico.cov()
corr_matrix = cancer_numerico.corr()

plt.figure(figsize=(20,20))
ax = sns.heatmap(corr_matrix,
                 vmax=1,
                 vmin=-1,
                 cbar_kws={"shrink":.8},
                 square=True,
                 annot=True,
                 fmt=".2f",
                 cmap="GnBu",
                 center=0)
plt.show()

#%%

# Para medias, sd y máximos

plt.figure(figsize=(15,7))

plt.subplot(1, 3, 1)
ax1=sns.heatmap(cancer_numerico[caracteristicas_media].corr(),
                xticklabels=False,
                yticklabels=False,
                cbar = False,
                square = True,
                annot=True, 
                fmt= '.2f',
                annot_kws={'size': 8},
                vmax=1, vmin=-1,
                cmap ='GnBu',
                center=0)
bottom, top = ax1.get_ylim()
ax1.set_ylim(bottom + 0.5, top - 0.5)

plt.subplot(1, 3, 2)
ax2=sns.heatmap(cancer_numerico[caracteristicas_sd].corr(),xticklabels=False, yticklabels=False , cbar = False,  square = True, annot=True, fmt= '.2f',annot_kws={'size': 8},vmax=1, vmin=-1, cmap ='GnBu',center=0)
bottom, top = ax2.get_ylim()
ax2.set_ylim(bottom + 0.5, top - 0.5)

plt.subplot(1, 3, 3)
ax3=sns.heatmap(cancer_numerico[caracteristicas_max].corr(),xticklabels=False, yticklabels=False , cbar = False,  square = True, annot=True, fmt= '.2f',annot_kws={'size': 8},vmax=1, vmin=-1, cmap ='GnBu',center=0)
bottom, top = ax2.get_ylim()
ax2.set_ylim(bottom + 0.5, top - 0.5)


#%%

####### COORDENADAS PARALELAS

from pandas.plotting import parallel_coordinates

caracteristicas_media.append("diagnosis")
parallel_coordinates(cancer_limpio_diagnostico[caracteristicas_media],
                     "diagnosis",
                     colormap='cool',
                     xticks=None)
plt.show()

#%%

####### CURVAS DE ANDREWS

from pandas.plotting import andrews_curves
andrews_curves(cancer_limpio_diagnostico[caracteristicas_media],
               "diagnosis",
               colormap='rainbow')
plt.show()


