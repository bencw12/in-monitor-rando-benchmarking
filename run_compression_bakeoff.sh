#!/bin/bash
# Experiment for Figure 3

CACHE_OPT=cache
MEM_ALLOC=256
OUT_DIR=./results/compression-bakeoff

if ! [[ ${1}  =~ ^[+-]?[0-9]+\.?[0-9]*$ ]]; then
    echo "Please enter the number of runs"
    exit 1
fi

NUM_RUNS=${1}

mkdir -p ${OUT_DIR}

for FILE in ${PWD}/kernels/compression-bakeoff/*; do
    ./run_batch.sh ${FILE} bzImage ${CACHE_OPT} ${MEM_ALLOC} ${NUM_RUNS} ${OUT_DIR}
done
