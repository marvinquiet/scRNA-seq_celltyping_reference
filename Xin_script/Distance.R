suppressMessages(library(anndata,lib.loc="/home/xwei44/miniconda3/envs/celltyping/lib/R/library"))

print("Compute Distance")

args <- commandArgs(trailingOnly = TRUE)
df_dir <- args[1]

ad_train <- read_h5ad(paste(dirname(df_dir),"train_adata.h5ad",sep = "/"))
ad_test <- read_h5ad(paste(dirname(df_dir),"test_adata.h5ad",sep = "/"))

cell_types <- unique(as.factor(ad_train$obs$cell.type))

method <- c("euclidean","maximum","manhattan", "canberra")
Eucli_dist <- rep(0,length(cell_types))
Weighted_distance = Overall_distance = rep(0,length(method))
Prop_dist=rep(0,length(method))

c=prop.table(table(ad_train$obs$cell.type))
d=prop.table(table(ad_test$obs$cell.type))

for(j in 1:length(method)){
for(i in 1:length(cell_types)){
    a=ad_test[which(ad_test$obs$cell.type==cell_types[i]),]
    b=ad_train[which(ad_train$obs$cell.type==cell_types[i]),]
    if(is.null(ncol(a))!=TRUE){
      a=colMeans(a)
    }
    if(is.null(ncol(b))!=TRUE){
      b=colMeans(b)
    }
    Eucli_dist[i]=dist(rbind(a,b),method = method[j])
}
Overall_distance[j]=dist(rbind(colMeans(ad_test),colMeans(ad_train)),method = method[j])
Weighted_distance[j]=prop.table(table(ad_train$obs$cell.type))%*%Eucli_dist
Prop_dist[j]=dist(rbind(c,d),method = method[j])
}

Distance = c(Overall_distance,Weighted_distance,Prop_dist)
Distance = log(Distance+0.01)

Print(Summary(Distance))

write(Distance, file.path(dirname(df_dir), "Distance.txt"))