# Exploration on selecting reference for scRNA-seq celltyping
The aim of this repo is to explore what might affect the quality of reference datasets for scRNA-seq celltyping. Thank Xin and Yajun for joining this project. Proud to have you all!

### What we know
- Pooling cells and individuals together as reference datasets can generate better prediction performance.
- Downsampling the pooled cells to a certain number, say originally 10,000 cells and we downsample to 5,000. This slightly decreases the performance of prediction but not that much. This is because of pooling effect which potentially removes the bias from individuals.
- There exists a satuation point when adding more individuals (See figure below). 

---
<img 
    src="./FigureS9.pdf" 
    raw=true
    width=400
/>

`The image describes the prediction of cell types in mouse brain.`

- (A) Intra-dataset prediction. Here, we have 7 mice in total (Mouse FC dataset) and we use one of them as target to predict major cell types. Then, we add individuals one by one (left panel) or pool all 6 together and add downsampled cells batch by batch (right pabel). As shown in the figure, when gradually adding individuals, the performance increases. However, for adding downsampled cells, the metrics are high at the beginning, but drop down a bit. Then, with more cells added, the prediction performance increases back. The result comes from 50 repetitions (with different sample seeds) and the solid line represents the average while the shade describes the 0.025 quantiles and 0.975 quantiles.
- (B) Inter-dataset prediction. We use 6 mice from Mouse pFC dataset and 3 mice from Mouse Allen dataset to predict one target in Mouse FC dataset on major cell types. 
- (C) Intra-dataset prediction. We use same Mouse FC dataset but predict sub-cell types. 
---

### What we want to know
- Does add a specific individual lower down the performance or not bring benefits to the prediction?
    - If so (most likely), what is special in this individual compared to others? For example, number of cells, biological condition, gene count distribution, mtDNA percentage and other characteristics.
- Does add an individual from different condition may also increase the performance?
    - We do observe that by combining individuals from different conditions can improve the performance in human PBMC experiments. But how much will it increase and what cause the increase? We need to quantify the selection of reference. 

---

### Resources

- Datasets
    - Mouse FC dataset: [paper](https://doi.org/10.1016/j.cell.2018.07.028), [data](http://dropviz.org/)
    - Mouse pFC dataset: [paper](https://doi.org/10.1038/s41467-019-12054-3), [data](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE124952) and information about clusters in saline samples only is [here](http://djeknad.pythonanywhere.com/download/)
    - Mouse Allen dataset: [paper](https://doi.org/10.1016/j.cell.2021.04.021), [data](https://portal.brain-map.org/atlases-and-data/rnaseq/mouse-whole-cortex-and-hippocampus-10x)
- Mouse brain performance from 50 repetitions
    - Accuracy/ARI/macroF1 metrics
    - Random sample list to indicate which individual is added


To-dos are listed and assigned through tissues. 
