# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 11:48:32 2020

@author: hp
"""
import numpy as np 
import scipy as sc
import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris

#%%

mean = [0, 0]
cov = [[1, 0], [0, 1]]  

x, y = np.random.multivariate_normal(mean, cov, 5000).T
plt.plot(x, y, 'o',alpha=0.2)
plt.axis('equal')
plt.show()


#%%

sns.set_style("white")
sns.kdeplot(x, y)

#%%

sns.kdeplot(x, y, cmap="Blues", shade=True, shade_lowest=True,n_levels=5)


#%%

# Contour plot with Iris dataset
df = sns.load_dataset('iris')

# Contour plot 2D básico
sns.set_style("white")
sns.kdeplot(df.sepal_width, df.sepal_length)

#%%

sns.kdeplot(df.sepal_width, df.sepal_length, cmap="Reds", shade=True, bw=.15,shade=True)

#%%

sns.kdeplot(df.sepal_width, df.sepal_length, cmap="Blues", shade=True)

#%%

from scipy.stats import multivariate_normal
from mpl_toolkits.mplot3d import Axes3D

mu_x = 0
mu_y = 0

x = np.linspace(-5,5,500)
y = np.linspace(-5,5,500)
X, Y = np.meshgrid(x,y)
pos = np.empty(X.shape + (2,))
pos[:, :, 0] = X; pos[:, :, 1] = Y
rv = multivariate_normal([mu_x, mu_y], [[1, 0], [0, 1]])

fig = plt.figure(figsize=(10,5))
ax = fig.gca(projection='3d')
ax.plot_surface(X, Y,rv.pdf(pos),cmap='viridis',linewidth=0)
ax.set_xlabel('X axis')
ax.set_ylabel('Y axis')
ax.set_zlabel('Z axis')
ax.auto_scale_xyz([-5, 5], [-5, 5], [0, 0.5])
plt.show()

CS = plt.contour(X, Y, rv.pdf(pos))

#%%

mu_x = 0
mu_y = 0

x = np.linspace(-5,5,500)
y = np.linspace(-5,5,500)
X, Y = np.meshgrid(x,y)
pos = np.empty(X.shape + (2,))
pos[:, :, 0] = X; pos[:, :, 1] = Y
rv = multivariate_normal([mu_x, mu_y], [[1, 0.7], [0.7, 1]])

fig = plt.figure(figsize=(10,5))
ax = fig.gca(projection='3d')
ax.plot_surface(X, Y, rv.pdf(pos),cmap='viridis',linewidth=0)
ax.set_xlabel('X axis')
ax.set_ylabel('Y axis')
ax.set_zlabel('Z axis')
ax.auto_scale_xyz([-5, 5], [-5, 5], [0, 0.5])
plt.show()

CS = plt.contour(X, Y, rv.pdf(pos))