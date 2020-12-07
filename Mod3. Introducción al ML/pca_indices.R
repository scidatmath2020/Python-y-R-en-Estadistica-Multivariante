indices <- read.csv("indices.csv")
colnames(indices)

indices <- indices[,c(2:10)]

n <- dim(indices)[1]
p <- dim(indices)[2]

pairs(indices,col="blue",pch=19,main="Tabla original")

###########

mu <- colMeans(indices[,2:9])
mu

S <- cov(indices[,2:9])
View(S)

########### Obtener las componentes principales

propios_S <- eigen(S)

propios_valores.S <- propios_S$values
propios_vectores.S <- propios_S$vectors

View(propios_vectores.S)

prop_var.S <- propios_valores.S/sum(propios_valores.S) #proporción de variabilidad
prop_var_acum.S <- cumsum(propios_valores.S)/sum(propios_valores.S) #proporción de variabilidad acumulada

##########
########## Obtener los componentes principales 
########## Notar que cada característica tiene 
##########

R <- cor(indices[,2:9])

propios_R <- eigen(R)

propios_valores.R <- propios_R$values
propios_vectores.R <- propios_R$vectors

prop_var.R <- propios_valores.R/sum(propios_valores.R) #proporción de variabilidad
prop_var_acum.R <- cumsum(propios_valores.R)/sum(propios_valores.R) #proporción de variabilidad acumulada

prop_var_acum.R

View(propios_vectores.R)

mean(propios_valores.R)

#########
######### Obtener los scores
#########

ones <- matrix(rep(1,n),nrow=n,ncol=1)

indices_centrado <- as.matrix(indices[,2:9]) - ones %*% mu
View(indices_centrado)

diagonal_S <- diag(diag(S))
View(diagonal_S)
  
indices_estandar <- indices_centrado %*% solve(diagonal_S)^(1/2)
View(indices_estandar)

scores <- indices_estandar %*% propios_vectores.R
colnames(scores) <- c("PC1","PC2","PC3","PC4","PC5","PC6","PC7","PC8")
row.names(scores) <- indices[,1]
  
View(scores)

#############
############# Graficar los scores
#############

pairs(scores,main="Scores",col="blue",pch=19)

#############
############# Screeplot
#############

screeplot(princomp(indices[,2:9],cor=T),main="Screeplot",col="blue",type="lines",pch=19)
# cor: valor lógico para indicar si queremos que los cálculos se hagan usando la matriz de 
#      correlación o la de covarianza

#############
############# Graficar los scores que nos interesen
#############

plot(scores[,c(1,2)],xlab="1er componente principal",ylab="2a componente principal",col="blue",
     pch=19,main="Primera y segunda componentes principales")
text(scores[,c(1,2)],labels=indices[,1],pos=1,col="blue",cex=0.4)

plot(scores[,c(1,3)],xlab="1er componente principal",ylab="3a componente principal",col="blue",
     pch=19,main="Primera y tercera componentes principales")
text(scores[,c(1,3)],labels=indices[,1],pos=1,col="blue")

plot(scores[,c(2,3)],xlab="2a componente principal",ylab="3a componente principal",col="blue",
     pch=19,main="Segunda y tercerda componentes principales")
text(scores[,c(2,3)],labels=indices[,1],pos=1,col="blue")

