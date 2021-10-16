'''
Configuration generation for running PBMC datasets
'''

import os, argparse

from pipelines import method_utils, dataloading_utils
from preprocess.process_train_test_data import *

if __name__ == "__main__":
    data_dir = "/home/wma36/gpu/data"

    ## parse arguments
    parser = argparse.ArgumentParser(description="Celltyping pipeline.")
    parser.add_argument('data_source', help="Load which dataset",
        choices=[
            'PBMC_batch1_ind', 'PBMC_batch1_ind_major', 'PBMC_batch1_ABC', 
            'PBMC_batch1_batchtoind', 'PBMC_batch1_multiinds', 'PBMC_batch1_multiinds_sample',
            'PBMC_batch2', 'PBMC_batch2_ind', 
            'PBMC_batch1_batch2_ind', 'PBMC_batch1_batch2_ind_major'
             ])

    parser.add_argument('-m', '--method', help="Run which method",
        choices=['MLP', 'SVM_RBF', 'SVM_linear'],
        required=True)
    parser.add_argument('--select_on', help="Feature selection on train or test, or None of them",
        choices=['train', 'test'])
    parser.add_argument('--select_method', help="Feature selection method, Seurat/FEAST or None",
            choices=['Seurat', 'FEAST', 'F-test'])
    parser.add_argument('--n_features', help="Number of features selected",
            default=1000, type=int)
    parser.add_argument('--train', help="Specify which as train", required=True)
    parser.add_argument('--test', help="Specify which as test", required=True)
    parser.add_argument('--sample_seed', help="Downsample seed in combined individual effect", 
            default=0, type=int)

    args = parser.parse_args()
    if args.data_source in ["PBMC_batch1_ind", "PBMC_batch1_ABC", "PBMC_batch2", 'PBMC_batch2_ind', 
            "PBMC_batch1_batchtoind", "PBMC_batch1_multiinds", "PBMC_batch1_batch2_ind"
            ]:
        pipeline_dir = "/home/wma36/gpu/scRNA-seq_celltyping_reference/Xin_dist_results/result_PBMC_batch1_inds_pairwise" ## for now, generate results under pairwise

    result_prefix = pipeline_dir+os.sep+"result_"+args.data_source+'_'+\
        args.train+'_to_'+args.test
    os.makedirs(result_prefix, exist_ok=True)

    ## create file directory 
    if args.select_on is None and args.select_method is None:
        result_dir = result_prefix+os.sep+"no_feature"
    else:
        result_dir = result_prefix+os.sep+args.select_method+'_'+\
                str(args.n_features)+'_on_'+args.select_on
    os.makedirs(result_dir, exist_ok=True)

    load_ind, train_adata, test_adata = load_adata(result_dir)
    if not load_ind:
        train_adata, test_adata = dataloading_utils.load_PBMC_adata(
            data_dir, result_dir, args=args)

        train_adata, test_adata = dataloading_utils.process_loaded_data(
                train_adata, test_adata, result_dir, args=args, scale=False)  ## no scale for calculating distance
        print("Train anndata: \n", train_adata)
        print("Test anndata: \n", test_adata)

    ## method_utils.run_pipeline(args, train_adata, test_adata, data_dir, result_dir)

    ## move distance calculation here
    Distance_RSCRIPT_PATH = "Distance.R"
    os.system("Rscript --vanilla " + Distance_RSCRIPT_PATH + " "+ result_dir)
 
