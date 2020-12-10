setwd("C:\\Users\\hp master\\OneDrive\\Escritorio\\distancias")

coordenadas <- read.csv("mx.csv")
names(coordenadas)

library(geosphere)

coordenadas <- coordenadas[,c(1,3,2)]
dim(coordenadas)

distancias <- function(x){
t(distm(coordenadas[x,2:3], 
      coordenadas[,2:3], fun = distHaversine)/1000)}

D <- as.data.frame(do.call(cbind,lapply(1:1991,distancias)))
colnames(D) <- coordenadas$city

D <- as.data.frame(cbind(coordenadas[,1],D))
colnames(D)[1] <- "ciudades"

###############################

data <- D[,2:1992]

mds.cities <- cmdscale(data,eig=TRUE)

plot(mds.cities$eig,pch=19,col="blue",xlab="Number","ylab"="Eigenvalor",type="o")
abline(a=0,b=0,col="red")

m <- sum(abs(mds.cities$eig[1:2])) / sum(abs(mds.cities$eig))
m

mds.cities <- cmdscale(data,eig=TRUE,k=2)

x1 <- mds.cities$points[,1]
x2 <- mds.cities$points[,2]


plot(x1,x2,pch=19,xlim=range(x1)+c(-1000,600),ylim=range(x2)+c(-500,500),col="red")
text(x1,x2,pos=4,labels=colnames(data),col="blue") 
