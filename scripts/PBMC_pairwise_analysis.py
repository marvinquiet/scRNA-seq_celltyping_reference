import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 18})
from textwrap import wrap

def summarize_PBMC_pairwise_result(result_dir):
    '''Summarize results under result_dir into dataframe
    '''
    metrics = ["Acc", "ARI", "macroF1"]

    res_dict = {}
    for root, dirs, files in os.walk(result_dir):
        for file in files:
            if "MLP_metrics.txt" in file:
                filepath = os.path.join(root, file)
                experiment_name = filepath.split('/')[-3]  ## get folder name
                res_dict[experiment_name] = {}
                with open(filepath, 'r') as fopen:
                    for line in fopen:
                        metric, value = line.strip().split(":")
                        if metric in metrics:
                            res_dict[experiment_name][metric] = float(value)
    df = pd.DataFrame.from_records(
        [
            (level1, level2, leaf)
            for level1, level2_dict in res_dict.items()
            for level2, leaf in level2_dict.items()
        ],
        columns=["experiment", "metrics", "value"]
    )

    ## formatting dataframe
    experiments = ["PBMC_batch1_ind", "PBMC_batch2_ind", "PBMC_batch1_batch2_ind"]
    exp_list = []
    for exp in df["experiment"]:
        for experiment in experiments:
            if experiment in exp:
                exp_list.append(experiment)
                break
    df["exp_type"] = exp_list  ## experiment type

    ref_list, target_list, effect_list = [], [], []
    for index, row in df.iterrows():
        ## get reference and target information
        ref_to_target = row["experiment"].replace('result_'+row["exp_type"]+'_', '')
        ref, target = ref_to_target.split('_to_')
        if row["exp_type"] == "PBMC_batch1_ind":
            ref_list.append(ref)
            target_list.append(target)
            effect_list.append("individual")
        if row["exp_type"] == "PBMC_batch2_ind":
            batch2_control_str = "control_"
            batch2_stim_str = "stimulated_"
            ## individual effects between same situations
            if batch2_control_str in ref and batch2_control_str in target:
                ref_list.append(ref.replace(batch2_control_str, ''))
                target_list.append(target.replace(batch2_control_str, ''))
                effect_list.append("individual")
            if batch2_stim_str in ref and batch2_stim_str in target:
                ref_list.append(ref.replace(batch2_stim_str, ''))
                target_list.append(target.replace(batch2_stim_str, ''))
                effect_list.append("individual") ## stimulated individual effect
            ## condition effect between batch2 individuals
            if batch2_control_str in ref and batch2_stim_str in target:
                ref_list.append(ref.replace(batch2_control_str, ''))
                target_list.append(target.replace(batch2_stim_str, ''))
                effect_list.append("clinical")
            if batch2_stim_str in ref and batch2_control_str in target:
                ref_list.append(ref.replace(batch2_stim_str, ''))
                target_list.append(target.replace(batch2_control_str, ''))
                effect_list.append("clinical")
        if row["exp_type"] == "PBMC_batch1_batch2_ind":
            batch1_str = "batch1_"
            batch2_control_str = "batch2control_"
            batch2_stim_str = "batch2stimulated_"
            ## batch effect
            if batch2_control_str in ref and batch1_str in target:
                ref_list.append(ref.replace(batch2_control_str, ''))
                target_list.append(target.replace(batch1_str, ''))
                effect_list.append("batch")
            if batch1_str in ref and batch2_control_str in target:
                ref_list.append(ref.replace(batch1_str, ''))
                target_list.append(target.replace(batch2_control_str, ''))
                effect_list.append("batch")
            if batch2_stim_str in ref and batch1_str in target:
                ref_list.append(ref.replace(batch2_stim_str, ''))
                target_list.append(target.replace(batch1_str, ''))
                effect_list.append("batch|clinical")
            if batch1_str in ref and batch2_stim_str in target:
                ref_list.append(ref.replace(batch1_str, ''))
                target_list.append(target.replace(batch2_stim_str, ''))
                effect_list.append("batch|clinical")
    df["ref"] = ref_list
    df["target"] = target_list
    df["effect"] = effect_list
            
    df.to_csv(result_dir+os.sep+'result_summary.csv')

def summarize_PBMC_pairwise_result_celltype():
    ## will need to summarize it in celltype specific accuracy
    pass

if __name__ == '__main__':
    result_dir = "/home/wma36/gpu/celltyping_refConstruct/pipelines/result_PBMC_collections/result_PBMC_batch1_inds_pairwise"
