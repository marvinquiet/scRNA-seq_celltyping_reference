'''
Load data for running celltyping experiments
'''
import os, sys
from preprocess.process_train_test_data import *

from preprocess.process_PBMC_train_test import *

#Distance_RSCRIPT_PATH = "Distance.R"

### === process loaded data
def process_loaded_data(train_adata, test_adata, result_dir, 
        args=None, scale=True, plot=True, 
        save_raw=False, save_data=True):

    if args is None:
        sys.exit("Error: Please check your argument parser object!")

    # curate for common cell types
    common_celltypes = set(train_adata.obs["cell.type"]).intersection(set(test_adata.obs["cell.type"]))
    train_cells = train_adata.obs.loc[train_adata.obs["cell.type"].isin(common_celltypes)].index
    test_cells = test_adata.obs.loc[test_adata.obs["cell.type"].isin(common_celltypes)].index
    train_adata = train_adata[train_cells]
    test_adata = test_adata[test_cells]

    if save_raw:
        train_adata.layers["counts"] = train_adata.X.copy() 
        test_adata.layers["counts"] = test_adata.X.copy() 

    ## feature selection
    train_adata, test_adata = feature_selection_train_test(train_adata, test_adata,
            result_dir, args.n_features, args.select_on, args.select_method)
    
    if save_data:
        save_adata(train_adata, test_adata, result_dir)

    #tmp_df_path2 = result_dir+os.sep+"tmp_counts.csv"
    #os.system("Rscript --vanilla " + Distance_RSCRIPT_PATH + " "+ tmp_df_path2)
    
    ## scale and analze
    train_adata, test_adata = scale_and_visualize(train_adata, test_adata,
        result_dir, scale=scale, plot=plot)

    return train_adata, test_adata

### === load PBMC anndata
def load_PBMC_adata(data_dir, result_dir, args=None, scale=True, plot=True):
    train_adata, test_adata = None, None
    ## === PBMC datasets
    if args.data_source == "PBMC_batch1_ind":
        train_adata, test_adata = \
            process_batch1_ind(data_dir, result_dir, 
                ind1=args.train, ind2=args.test)
    if args.data_source == "PBMC_batch1_ind_major":
        train_adata, test_adata = \
            process_batch1_ind(data_dir, result_dir, 
                ind1=args.train, ind2=args.test,
                celltype_gran=0)
    if args.data_source == "PBMC_batch1_ABC":
         train_adata, test_adata = \
             process_batch1_ABC(data_dir, result_dir, 
                 batch1=args.train, batch2=args.test)
    if args.data_source == "PBMC_batch1_batchtoind":
         train_adata, test_adata = \
                 process_batch1_batchtoind(data_dir, result_dir,
                         batch=args.train, ind=args.test, sample=True, sample_seed=0)
    if args.data_source == "PBMC_batch1_multiinds":
        train_adata, test_adata = \
                process_batch1_multiinds(data_dir, result_dir,
                        sample_ind=args.train, pred_ind=args.test,
                        sample=False)
    if args.data_source == "PBMC_batch1_multiinds_sample":
        train_adata, test_adata = \
                process_batch1_multiinds(data_dir, result_dir,
                        sample_ind=args.train, pred_ind=args.test,
                        sample=True, sample_seed=args.sample_seed)
    if args.data_source == "PBMC_batch2":
        train_adata, test_adata = \
            process_batch2_ctrl_stim(data_dir, result_dir, 
                cond1=args.train, cond2=args.test)
    if args.data_source == "PBMC_batch2_ind":
        train_adata, test_adata = \
            process_batch2_ind(data_dir, result_dir,
                input1=args.train, input2=args.test)
    if args.data_source == "PBMC_batch1_batch2_ind":
        train_adata, test_adata = \
            process_batch1_batch2_ind(data_dir, result_dir,
                    input1=args.train, input2=args.test)
    if args.data_source == "PBMC_batch1_batch2_ind_major":
        train_adata, test_adata = \
             process_batch1_batch2_ind(data_dir, result_dir,
                    input1=args.train, input2=args.test,
                    celltype_gran=0)

    return train_adata, test_adata
