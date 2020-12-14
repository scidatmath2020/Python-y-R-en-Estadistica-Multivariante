rm(list=ls())
library(MASS)
library(mclust)
library(cluster)

muestra <- read.csv("mixturas3.csv")
plot(muestra$u.1,muestra$u.2)

names(muestra)

mclust.muestra <- Mclust(muestra[,2:3],modelNames = c("VVV"))
grupos.muestra <- mclust.muestra$classification
summary(as.factor(grupos.muestra))

colores.grupos <- c("blue","red","green")[grupos.muestra]
pairs(muestra[,2:3],col=colores.grupos)

clusplot(muestra[,2:3],grupos.muestra)

mclust.muestra$parameters
