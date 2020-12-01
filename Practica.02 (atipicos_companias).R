install.packages("tidyverse",dependencies = TRUE)
install.packages("dplyr")

library(MASS)
library(stats)
library(tidyverse)

library(ggpubr)

setwd("C:/Users/hp master/Documents/SciData/Est_Mult")
companias <- read.csv("companies79.csv")
companias <- companias[,2:9]

Xf <-  companias[,2:7]
Xlog <- log(Xf)

Xf.kde <- kde2d(Xf[,"V4"], Xf[,"V5"],n=50)   # MASS package
Xlog.kde <- kde2d(Xlog[,"V4"], Xlog[,"V5"],n=50)

image(Xf.kde)       
contour(Xf.kde, add = TRUE)     

image(Xlog.kde)       
contour(Xlog.kde, add = TRUE)     

plot(Xf[,"V4"],Xf[,"V5"])
contour(Xf.kde, add = TRUE)     


plot(Xlog[,"V4"],Xlog[,"V5"])
contour(Xlog.kde, add = TRUE)   


medias_Xf <- colMeans(Xf)
sigma_Xf <- cov(Xf)

d_M <- mahalanobis(Xf,medias_Xf,sigma_Xf)

d_M_ordenada <- sort(d_M,decreasing = TRUE)

umbral <- qchisq(0.95,df=6)

companias$d_M <- d_M

companias[companias$d_M > umbral,c("V1","d_M")]

companias$atipico <- ifelse(companias$d_M > umbral, "Sí atípico", "No atípico")

original <- ggplot(data = companias) +
  geom_point(mapping = aes(x=V2,y=V3,color = atipico)) +
  scale_color_manual(values=c("blue", "red"))

original

out <- companias[companias$atipico == "Sí atípico",]

companias_clean <- companias[companias$atipico == "No atípico",]

Xclean <- companias_clean[,c(2:7)]

medias_Xclean <- colMeans(Xclean)

medias_Xclean
medias_Xf

sigma_Xclean <- cov(Xclean)

companias_clean$d_M_clean <- mahalanobis(Xclean,medias_Xclean,sigma_Xclean)

companias_clean$atipico_clean <- ifelse(companias_clean$d_M_clean > umbral, "Sí atípico", "No atípico")


clean <- ggplot(data = companias_clean) +
  geom_point(mapping = aes(x=V2,y=V3,color = atipico_clean)) +
  scale_color_manual(values=c("blue", "red"))


ggarrange(original,clean,labels = c("Original","Limpios"),ncol=2,nrow=1)



