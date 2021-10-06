#!/bin/bash
#SBATCH --job-name=PBMC
#SBATCH --output=celltyping_PBMC_samplewise.out
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=32

source ~/.bashrc
conda activate /home/wma36/gpu/envs/celltyping

cd /home/wma36/gpu/celltyping_refConstruct

PIPELINE_DIR="/home/wma36/gpu/celltyping_refConstruct/pipelines"
method="MLP"

## === PBMC batch1 individual
task="PBMC_batch1_ind"
test="1085"
declare -a inds=("1154" "1043" "1079" "1249" "1493" "1511" "1598")

## from https://stackoverflow.com/questions/1527049/how-can-i-join-elements-of-an-array-in-bash/53050617
function join_by { local d=${1-} f=${2-}; if shift 2; then printf %s "$f" "${@/#/$d}"; fi; }
## exclude one individual and predict
for ind_exclude in ${inds[@]}; do
    excluded_list=${inds[@]/$ind_exclude}
    train=$(join_by _ $excluded_list)
    python -m pipelines.PBMC_pipeline $task -m $method --select_on train --select_method F-test --train $train --test $test
done
## use all to predict
train=$(join_by _ ${inds[@]})
echo $train
python -m pipelines.PBMC_pipeline $task -m $method --select_on train --select_method F-test --train $train --test $test

conda deactivate
