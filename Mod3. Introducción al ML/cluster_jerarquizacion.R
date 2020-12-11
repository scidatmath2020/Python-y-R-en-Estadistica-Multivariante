mx_extendido <- read.csv("mx_extendido.csv")

names(mx_extendido)

row.names(mx_extendido) <- mx_extendido[,1]

View(mx_extendido)

data <- mx_extendido[,-1]
names(data)

data$capital <- as.factor(data$capital)
data$cod_entidad <- as.factor(data$cod_entidad)

names(data)

##################################################################
#########  Cálculo de las distancias
##################################################################

gower_df <- daisy(data,
                  metric = "gower" ,
                  type = list(logratio = 4))

summary(gower_df)

View(as.matrix(gower_df))

##################################################################
#########  AGNES
##################################################################

#### single (complete,average,ward)

agnes_data <- agnes(gower_df,diss=TRUE,method="single")

####### dendograma

plot(agnes_data,main="Dendograma AGNES por single")

#### Tomando K_agnes clusters

K_agnes = 2#indica el número de clusters
  
rect.hclust(agnes_data,k=K_agnes,border="blue") #dibuja los clusters en el dendograma

#### Asignación de cada observación a un cluster

grupos_agnes <- cutree(agnes_data,K_agnes)  # asigna el grupo a cada observación
grupos_agnes

####

plot(silhouette(grupos_agnes,gower_df))

##################################################################
#########  DIANA
##################################################################

diana_data <- diana(gower_df,diss=TRUE,metric="euclidean")

plot(diana_data,main="Dendograma DIANA")

#### Tomando K_diana clusters

K_diana = 4#indica el númerod de clusters

rect.hclust(diana_data,k=K_diana,border="blue")

#### Asignación de cada observación a un cluster

grupos_diana <- cutree(diana_data,K_diana)  # asigna el grupo a cada observación
grupos_diana

####

plot(silhouette(grupos_diana,gower_df))

