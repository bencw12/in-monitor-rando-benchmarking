#!/bin/bash
# Experiment for Figure 4

MEM_ALLOC=256
OUT_DIR=./results/cache-effects

if ! [[ ${1}  =~ ^[+-]?[0-9]+\.?[0-9]*$ ]]; then
    echo "Please enter the number of runs"
    exit 1
fi

NUM_RUNS=${1}

mkdir -p ${OUT_DIR}

for CACHE_OPT in no-cache cache; do
    for kernel in lupine4 aws ubuntu; do
        ./run_batch.sh ./kernels/lz4/bzImage-${kernel}-nokaslr-lz4 bzImage ${CACHE_OPT} ${MEM_ALLOC} ${NUM_RUNS} ${OUT_DIR}
        ./run_batch.sh ./kernels/uncompressed/vmlinux-${kernel}-nokaslr nokaslr ${CACHE_OPT} ${MEM_ALLOC} ${NUM_RUNS} ${OUT_DIR}
    done
done