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
    - If so (most likely), what is special in this individual compared to others?
    






---

### Resources

- Datasets
    - Mouse FC dataset
    - Mouse pFC dataset
    - Mouse Allen dataset
- Performance from 50 datasets
    - Random seed list
