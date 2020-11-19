# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 13:21:23 2020

@author: hp
"""


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.offline as ply


from plotly.offline import plot


#%%

iris = pd.read_csv("C:/Users/hp master/Documents/SciData/Est_Mult\Mod01. Espacios multivariantes/C01. Mediciones con multiples variables/iris.csv")
iris.head()

iris = iris.drop("Unnamed: 0",axis=1)
iris.head()


#%%

iris.shape

iris["Species"].value_counts()

#%%

'''BOXPLOTS'''

sns.set(style="ticks", palette="muted")
ax = sns.boxplot(x="Species", y="Petal.Length", data=iris)
ax

#%%

'''boxplots para cada variable divididos por especie'''

iris.boxplot(by="Species",figsize=(12,6))

#%%

'''HISTOGRAMAS'''

iris.hist(edgecolor="black",linewidth=0.2,grid=False,figsize=(12,6))

#%%

iris.describe()

#%%
'''Histograma de una variable por categorías'''

plt.hist(iris[iris["Species"]=="setosa"]["Petal.Length"],alpha=0.5,bins=10)
plt.hist(iris[iris["Species"]=="versicolor"]["Petal.Length"],alpha=0.5,bins=10)
plt.hist(iris[iris["Species"]=="virginica"]["Petal.Length"],alpha=0.5,bins=10)
plt.show()
#%%

'''Densidad kernel'''

## UNIVARIABLE

sns.distplot(iris["Petal.Length"],bins=10)
plt.show()

## Varias columnas
sns.distplot(iris[iris["Species"]=="setosa"]["Petal.Length"],bins=10)
sns.distplot(iris[iris["Species"]=="versicolor"]["Petal.Length"],bins=10)
sns.distplot(iris[iris["Species"]=="virginica"]["Petal.Length"],bins=10)

#%%

'''Scatterplot'''

colores = pd.DataFrame({"Cod":["red","blue","green"],"Species":["setosa","versicolor","virginica"]})
iris = iris.join(colores.set_index(["Species"]),on=["Species"],how="inner")

plt.scatter(iris["Petal.Length"],iris["Petal.Width"], s=200,c=iris["Cod"],marker='.',alpha=0.5)

#########  alternativa
sns.FacetGrid(iris,hue="Species",height=5).map(plt.scatter,"Petal.Length","Petal.Width").add_legend()

######### scatter con histogramas

sns.jointplot(x="Petal.Length",y="Petal.Width",data=iris)

######## scatter 3d

fig = px.scatter_3d(iris,x="Sepal.Length",y="Sepal.Width",z="Petal.Width",color="Species")
plot(fig)

######## scatter matrix

sns.pairplot(iris,hue="Species")


sns.pairplot(iris,hue="Species",diag_kind="hist")

#%%
'''Medidas descriptivas'''

cov_iris = iris.cov()
corr_iris = iris.corr()

plt.figure(figsize=(8,6))
ax = sns.heatmap(iris.corr(), annot=True, linecolor='white',linewidths=0.3, fmt='.2f', cbar=True, cmap="GnBu")

#%%
'''Coordenadas paralelas'''

from pandas.plotting import parallel_coordinates
from pandas.plotting import andrews_curves

parallel_coordinates(iris,"Species",colormap="rainbow")

''' Curvas de Andrews '''

andrews_curves(iris, "Species", colormap="rainbow")

'''Radar: ver https://python-graph-gallery.com/radar-chart/'''



