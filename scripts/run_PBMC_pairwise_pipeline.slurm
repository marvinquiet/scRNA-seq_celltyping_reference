#!/bin/bash
#SBATCH --job-name=PBMC
#SBATCH --output=celltyping_PBMC_pairwise_crossbatch.out
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=32

source ~/.bashrc
conda activate /home/wma36/gpu/envs/celltyping

cd /home/wma36/gpu/celltyping_refConstruct

PIPELINE_DIR="/home/wma36/gpu/celltyping_refConstruct/pipelines"
method="MLP"

## from https://stackoverflow.com/questions/1527049/how-can-i-join-elements-of-an-array-in-bash/53050617
function join_by { local d=${1-} f=${2-}; if shift 2; then printf %s "$f" "${@/#/$d}"; fi; }


## === PBMC batch1 individual
declare -a batch1_inds=("1154" "1043" "1079" "1249" "1493" "1511" "1598" "1085")

task="PBMC_batch1_ind"
#for ind1 in ${batch1_inds[@]}; do
#    for ind2 in ${batch1_inds[@]}; do
#        if [ "$ind1" != "$ind2" ]; then
#            echo "$ind1 $ind2"
#            python -m pipelines.PBMC_pipeline $task -m $method --select_on train --select_method F-test --train $ind1 --test $ind2
#        fi
#    done
#done


## === PBMC batch2 individual
declare -a batch2_inds=("control_101" "control_1015" "control_1016" "control_1039" "control_107" "control_1244" "control_1256" "control_1488" "stimulated_101" "stimulated_1015" "stimulated_1016" "stimulated_1039" "stimulated_107" "stimulated_1244" "stimulated_1256" "stimulated_1488")

#task="PBMC_batch2_ind"
#for ind1 in ${batch2_inds[@]}; do
#    for ind2 in ${batch2_inds[@]}; do
#        if [ "$ind1" != "$ind2" ]; then
#            echo "$ind1 $ind2"
#            python -m pipelines.PBMC_pipeline $task -m $method --select_on train --select_method F-test --train $ind1 --test $ind2
#        fi
#    done
#done

## PBMC batch1 individual to batch2 individual
task="PBMC_batch1_batch2_ind"
for ind1 in ${batch1_inds[@]}; do
    batch1_ind="batch1_$ind1"
    for ind2 in ${batch2_inds[@]}; do
        batch2_ind="batch2$ind2"
        echo "$batch1_ind $batch2_ind"
        python -m pipelines.PBMC_pipeline $task -m $method --select_on train --select_method F-test --train $batch1_ind --test $batch2_ind
        python -m pipelines.PBMC_pipeline $task -m $method --select_on train --select_method F-test --train $batch2_ind --test $batch1_ind
    done
done


conda deactivate
