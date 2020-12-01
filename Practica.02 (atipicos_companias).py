# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 14:31:48 2020

@author: hp
"""
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import scipy as sc
#%%
companias = pd.read_csv("C:/Users/hp master/Documents/SciData/Est_Mult/companies79.csv")

companias.drop("Unnamed: 0",axis=1,inplace=True)

companias.head()

#%%

Xf = companias.drop(["V1","V8"],axis=1)

Xlog = np.log(Xf)

#%%

sns.kdeplot(Xf["V4"], Xf["V5"], cmap="Blues", shade=False, shade_lowest=True)

sns.kdeplot(Xlog["V4"], Xlog["V5"], cmap="Blues", shade=False, shade_lowest=True)

Xf[["V4","V5"]].describe()

Xlog[["V4","V5"]].describe()

#%%

plt.plot(Xf["V4"], Xf["V5"], 'o',alpha=0.2)
plt.plot(Xlog["V4"], Xlog["V5"], 'o',alpha=0.2)

#%%

mu = np.mean(Xf)
SX = Xf.cov()

Xf.loc[0]
Xf.head(1)

d_M = []

for i in range(0,79):
    d_M.append(sc.spatial.distance.mahalanobis(Xf.loc[i], mu, np.linalg.inv(SX)) ** 2)
    
sorted(d_M,reverse=True)

#%%

umbral = sc.stats.chi2.ppf(0.975, 6)
umbral

companias["d_M"] = d_M

companias[companias["d_M"]>umbral].head()

companias["atipico"] = np.where(companias["d_M"]>umbral,"Sí atípico","No atípico")
companias["color"] = np.where(companias["d_M"]>umbral,"red","blue")

companias.head()

#%%

plt.scatter(companias["V2"],companias["V3"],
            s=200,c=companias["color"],marker='.',alpha=0.5)

#%%

out = companias[companias["d_M"]>umbral]

companias_clean = companias[companias["d_M"]<=umbral]

#%%

Xclean = companias_clean[["V2","V3","V4","V5","V6","V7"]]

mu_clean = np.mean(Xclean)

mu_clean
mu

SX_clean = Xclean.cov()

SX_clean

#%%

Xclean.shape
Xclean.set_index(pd.Index(list(range(0,69))),inplace=True)
d_M_clean = []

for i in range(0,69):
    d_M_clean.append(sc.spatial.distance.mahalanobis(Xclean.loc[i],
                                                     mu_clean,
                                                     np.linalg.inv(SX_clean)) ** 2)

companias_clean["d_M_clean"] = d_M_clean

companias_clean["atipico_clean"] = np.where(companias_clean["d_M_clean"]>umbral,
                                            "Sí atípico","No atípico")

companias_clean["color_clean"] = np.where(companias_clean["d_M_clean"]>umbral,
                                            "red","blue")

#%%

plt.scatter(companias_clean["V2"],companias_clean["V3"],
            s=200,c=companias_clean["color_clean"],marker='.',alpha=0.5)

