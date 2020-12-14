rm(list=ls())
regiones <- read.csv("regiones.csv")

install.packages("class")
library(class)

regiones.X <- regiones[1:300,2:3]
regiones.Y <- regiones[1:300,4]

n <- dim(regiones.X)[1]

knn.clase <- list()
knn.tablas <- list()
knn.errores <- vector()

length(regiones.Y)
set.seed(2020)
for(K in 1:20){
  knn.clase[[K]] <- knn.cv(regiones.X,regiones.Y,k=K)
  knn.tablas[[K]] <- table(regiones.Y,knn.clase[[K]])
  knn.errores[K] <- n-sum(regiones.Y==knn.clase[[K]])
}

knn.errores

which(knn.errores==min(knn.errores))

knn.tablas[[1]]
knn.errores[[1]]

100*knn.errores[[1]]/n

knn.clase[[1]]
regiones.X$clasificador <- knn.clase[[1]]

regiones.X$codigo_clasificador <- ifelse(regiones.Y==regiones.X$clasificador,TRUE,FALSE)

# Grafico: buenas en rojo; malas en negro
plot(regiones.X$x1,regiones.X$x2,pch=19,col=(regiones.X$codigo_clasificador+1))

x0 <- c(regiones[301,])

distancias <- sqrt((regiones[1:300,2]-x0[[2]])^2+(regiones[1:300,3]-x0[[3]])^2)

x0[[4]] == regiones.Y[which(distancias == min(distancias))]

#####################
#####################
#####################

mixturas <- read.csv("mixturas4.csv")

X <- mixturas[,1:2]
Y <- mixturas[,3]

n <- nrow(X)
p <- ncol(X)

### LDA

LDA <- lda(Y~.,data=X,CV=TRUE) #qda(Y~.,data=X,CV=TRUE) si se quiere cuadrático

LDA$class #nuevas clasificaciones

### Tabla de contingencias

tabla <- table(Y,LDA$class)
tabla

#### Errores

errores <- n-sum(Y==LDA$class)
100*errores/n




