suppressMessages(library(anndata))

print("Compute Distance")

args <- commandArgs(trailingOnly = TRUE)
df_dir <- args[1]

print(df_dir)

ad_train <- read_h5ad(paste(df_dir,"train_adata.h5ad",sep = "/"))
ad_test <- read_h5ad(paste(df_dir,"test_adata.h5ad",sep = "/"))

cell_types <- sort(unique(as.factor(ad_train$obs$cell.type)))

method <- c("euclidean","maximum","manhattan", "canberra")
Eucli_dist <- rep(0,length(cell_types))
Weighted_distance = Overall_distance = rep(0,length(method))
Prop_dist=rep(0,length(method))

c=prop.table(table(ad_train$obs$cell.type))
d=prop.table(table(ad_test$obs$cell.type))

for(j in 1:length(method)){
    for(i in 1:length(cell_types)){
        a=ad_test[which(ad_test$obs$cell.type==cell_types[i]),]$X
        ## here: a is anndata object if not using $X
        b=ad_train[which(ad_train$obs$cell.type==cell_types[i]),]$X
        if(is.null(ncol(a))!=TRUE){
          a=colMeans(as.matrix(a))  ## Error in colMeans(a) : 'x' must be an array of at least two dimensions, need to convert to matrix
        }
        if(is.null(ncol(b))!=TRUE){
          b=colMeans(as.matrix(b))
        }
        Eucli_dist[i]=dist(rbind(a,b),method = method[j])
}
Overall_distance[j]=dist(rbind(colMeans(as.matrix(ad_test$X)),
                               colMeans(as.matrix(ad_train$X))),
                               method = method[j])
Weighted_distance[j]=prop.table(table(ad_train$obs$cell.type))%*%Eucli_dist
Prop_dist[j]=dist(rbind(c,d),method = method[j])
}

Distance = c(Overall_distance, Weighted_distance, Prop_dist)
## Distance = log(Distance+0.01)

print(summary(Distance)) ## Bug fix: change to small capital print() and summary()

write(Distance, file.path(df_dir, "Distance.txt"))
