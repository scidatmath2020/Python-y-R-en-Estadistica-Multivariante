# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 12:10:10 2020

@author: hp
"""

'''Digamos que medimos dos variables que no están Normalmente distribuidas.
Por ejemplo, observamos varios ríos y para cada río observamos el nivel máximo
de ese río durante un cierto período de tiempo. Además, también contamos 
cuántos meses cada río causó inundaciones. La distribución de probabilidad del 
nivel máximo del río es una Gumbel. La cantidad de veces que se produjo una 
inundación se modela de acuerdo con una distribución Beta.

Es bastante razonable suponer que el nivel máximo y el número de inundaciones 
van a estar correlacionados. Si un río crece demasiado es probable que también 
haya inundaciones. Sin embargo, aquí nos encontramos con un problema: ¿cómo 
debemos modelar esa distribución de probabilidad? Arriba solo especificamos 
las distribuciones para las variables individuales, independientemente de la 
otra (es decir, las marginales). En realidad, estamos lidiando con una 
distribución conjunta de ambas variables juntas.'''

#%%

# Veamos la utilidad de las funciones cópulas.
import scipy as sc
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
# Vamos a generar datos uniformemente distribuidos
x = stats.uniform(0, 1).rvs(10000)
sns.distplot(x, kde=False, norm_hist=True)

#%%

'''A continuación, queremos transformar estas muestras para que, en lugar de 
uniformes, ahora estén Normalmente distribuidas. La transformación que hace 
esto es la inversa de la función de distribución (o densidad acumulada) (CDF) 
de la distribución normal (que podemos obtener en scipy.stats con ppf):'''

norm = stats.distributions.norm()
x_trans = norm.ppf(x)
sns.distplot(x_trans)

#%%

'''
Si trazamos ambas juntas, podemos obtener una intuición de cómo se ve la CDF 
inversa y cómo funciona:
'''

h = sns.jointplot(x, x_trans, stat_func=None)
h.set_axis_labels('original', 'transformed', fontsize=16)

'''
La CDF inversa estira las regiones externas de la uniforme para producir una 
normal.
'''

#%%
'''
Podemos hacer esto para distribuciones de probabilidad arbitrarias 
(univariadas), como la Beta:'''

beta = stats.distributions.beta(a=10, b=3)
x_trans = beta.ppf(x)
h = sns.jointplot(x, x_trans, stat_func=None)
h.set_axis_labels('orignal', 'transformed', fontsize=16)


#%%

'''
O la Gumbel:
'''

gumbel = stats.distributions.gumbel_l()
x_trans = gumbel.ppf(x)
h = sns.jointplot(x, x_trans, stat_func=None)
h.set_axis_labels('original', 'transformed', fontsize=16)

#%%

'''
Para hacer la transformación opuesta de una distribución arbitraria a la 
Uniforme(0, 1) simplemente aplicamos la inversa de la CDF inversa, es decir, 
la CDF:
'''

x_trans_trans = gumbel.cdf(x_trans)
h = sns.jointplot(x_trans, x_trans_trans, stat_func=None)
h.set_axis_labels('original', 'transformed', fontsize=16);

#%%
'''
Bien, entonces sabemos cómo transformar de cualquier distribución a una 
uniforme, y viceversa. En matemáticas, esto se llama la transformación 
integral de probabilidad.

¿Cómo nos ayuda esto con nuestro problema de crear una distribución de 
probabilidad conjunta personalizada? En realidad ya casi hemos terminado. 
Sabemos cómo convertir cualquier cosa distribuida uniformemente en una 
distribución de probabilidad arbitraria. Eso significa que solo necesitamos 
generar datos distribuidos uniformemente con las correlaciones que queremos.

¿Como hacemos eso?

    1) Simulamos a partir de una Gaussiana multivariante con la estructura de 
correlación específica que queremos.
    2) Transformamos para que las marginales sean uniformes.
    3) Transformamos las marginales uniformes a lo que queramos.

Vamos a crear muestras a partir de una Normal multivariante correlacionada:
'''

# Generando la Normal multivariante con correlaciones .5
mvnorm = stats.multivariate_normal(mean=[0, 0], cov=[[1., 0.5], 
                                                     [0.5, 1.]])

x = mvnorm.rvs(100000)

h = sns.jointplot(x[:, 0], x[:, 1], kind='kde', stat_func=None)
h.set_axis_labels('X1', 'X2', fontsize=16)

#%%

'''
Ahora usaremos lo que aprendimos arriba para "uniformizar" las marginales. 
Este diagrama conjunto suele ser cómo se visualizan las cópulas.
'''

norm = stats.norm()
x_unif = norm.cdf(x)
h = sns.jointplot(x_unif[:, 0], x_unif[:, 1], kind='hex', stat_func=None)
h.set_axis_labels('Y1', 'Y2', fontsize=16);

#%%

'''
Ahora solo transformamos los marginales nuevamente a lo que queremos 
(Gumbel y Beta):
'''

m1 = stats.gumbel_l()
m2 = stats.beta(a=10, b=2)

x1_trans = m1.ppf(x_unif[:, 0])
x2_trans = m2.ppf(x_unif[:, 1])

h = sns.jointplot(x1_trans, x2_trans, kind='kde', xlim=(-6, 2), ylim=(.6, 1.0), stat_func=None)
h.set_axis_labels('Maximum river level', 'Probablity of flooding', fontsize=16)

#%%

'''
Contrastemos eso con la distribución conjunta sin correlaciones:
'''

x1 = m1.rvs(10000)
x2 = m2.rvs(10000)

h = sns.jointplot(x1, x2, kind='kde', xlim=(-6, 2), ylim=(.6, 1.0), stat_func=None)
h.set_axis_labels('Maximum river level', 'Probablity of flooding',  fontsize=16)

#%%
'''
Entonces, al usar la distribución Uniforme como nuestra base, podemos inducir 
fácilmente correlaciones y construir de manera flexible distribuciones de 
probabilidad complejas. Todo esto se extiende directamente a distribuciones de 
dimensiones superiores también.
'''
