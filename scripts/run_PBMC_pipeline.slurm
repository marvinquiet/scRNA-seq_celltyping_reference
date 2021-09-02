#!/bin/bash
#SBATCH --job-name=PBMC
#SBATCH --output=celltyping_PBMC_cross_Ding.out
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=32

source ~/.bashrc
conda activate /home/wma36/gpu/envs/celltyping

cd /home/wma36/gpu/celltyping_refConstruct

PIPELINE_DIR="/home/wma36/gpu/celltyping_refConstruct/pipelines"

declare -a celltyping_python=("MLP" "GEDFN" "ItClust" "RF" "SVM_RBF" "SVM_linear")

## ==== PBMC batch1 S1 -> S5
task="PBMC_batch1_ind"
train="1154"
test="1085"


## python pipeline
for method in ${celltyping_python[@]}; do
    python -m pipelines.PBMC_pipeline $task -m $method --train $train --test $test
    python -m pipelines.PBMC_pipeline $task -m $method --select_on train --select_method Seurat --train $train --test $test
    python -m pipelines.PBMC_pipeline $task -m $method --select_on test --select_method Seurat --train $train --test $test
    python -m pipelines.PBMC_pipeline $task -m $method --select_on train --select_method FEAST --train $train --test $test
    python -m pipelines.PBMC_pipeline $task -m $method --select_on train --select_method F-test --train $train --test $test
    python -m pipelines.PBMC_pipeline $task -m $method --select_on test --select_method FEAST --train $train --test $test
done

conda deactivate
