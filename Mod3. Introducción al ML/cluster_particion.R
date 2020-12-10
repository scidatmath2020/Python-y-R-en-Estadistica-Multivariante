install.packages("cluster")
library(cluster)
###################################

set.seed(2020)
data <- iris[sample(1:150,150),]

Data <- iris[,1:4]
n <- dim(Data)[1]

########### Selección de K y cálculo de los grupos

wcss <- vector()
for(k in 1:20){
  wcss[k] <- sum(kmeans(Data,k,nstart=25)$withinss)
}

plot(x=1:20,y=wcss,pch=19,col="blue",type="o")

#########

K=3

Kmeans <- kmeans(Data,centers=K,nstart=25)

##### Cálculo de SCDG y porcentaje bien clasificado

SCDG <- Kmeans$withinss
SCDG # SCDG de cada grupo
Kmeans$tot.withinss #SCDG total

100 * Kmeans$betweenss / Kmeans$totss #porcentaje bien clasificado

##### Grupos:

grupos.Kmeans <- Kmeans$cluster
grupos.Kmeans

##### Scatterplot matrix con la división de grupos resultante

col.Kmeans <- c("blue","red","green")[grupos.Kmeans]
pairs(Data,col=col.Kmeans,main="K-medias",pch=19)

##### Graficación

clusplot(Data, Kmeans$cluster, color=T, shade=T, labels=0, lines=0)

##### Cálculo de las siluetas

dist.euclidea <- dist(Data,method="euclidean")
silueta.Kmeans <- silhouette(grupos.Kmeans,dist.euclidea)
plot(silueta.Kmeans,main="Silueta",col="blue")

#######################################
######## Método de particiones PAM
#######################################

dist.euclidea <- dist(Data,method="euclidean")

skm <- vector()

for(i in 2:20){
  Kmedoids <- pam(dist.euclidea,i)
  grupos.Kmedoids <- Kmedoids$cluster
  silueta.Kmedoids <- silhouette(grupos.Kmedoids,dist.euclidea)
  skm[i] <- summary(silueta.Kmedoids)$avg.width
}

skm[1]=0

plot(x=1:20,y=skm,pch=19,col="blue",type="o")

Kmedoids <- pam(Data,3)
Kmedoids

grupos.Kmedoids <- Kmedoids$clustering
grupos.Kmedoids

col.Kmedoids <- c("blue","red","green")[grupos.Kmedoids]
pairs(Data,col=col.Kmedoids,main="PAM",pch=19)

clusplot(Data, Kmedoids$clustering, color=T, shade=T, labels=0, lines=0)

dist.euclidea <- dist(Data,method="euclidean")
silueta.Kmeans <- silhouette(grupos.Kmedoids,dist.euclidea)
plot(silueta.Kmeans,main="Silueta",col="blue")
