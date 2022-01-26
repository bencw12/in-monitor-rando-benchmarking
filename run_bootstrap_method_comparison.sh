#!/bin/bash
# Experiment for Figure 6

MEM_SIZE=256
CACHE_OPT=cache
OUT_DIR=./results/bootstrap-comparison

if ! [[ ${1}  =~ ^[+-]?[0-9]+\.?[0-9]*$ ]]; then
    echo "Please enter the number of runs"
    exit 1
fi

NUM_RUNS=${1}

mkdir -p ${OUT_DIR}

for kernel in lupine4 aws ubuntu; do
    ./run_batch.sh ./kernels/compression-none/bzImage-${kernel}-nokaslr-none bzImage ${CACHE_OPT} ${MEM_SIZE} ${NUM_RUNS} ${OUT_DIR}
    ./run_batch.sh ./kernels/lz4/bzImage-${kernel}-nokaslr-lz4 bzImage ${CACHE_OPT} ${MEM_SIZE} ${NUM_RUNS} ${OUT_DIR}
    ./run_batch.sh ./kernels/optimized-compression-none/bzImage-${kernel}-nokaslr-none-optimized bzImage ${CACHE_OPT} ${MEM_SIZE} ${NUM_RUNS} ${OUT_DIR}
    ./run_batch.sh ./kernels/uncompressed/vmlinux-${kernel}-nokaslr nokaslr ${CACHE_OPT} ${MEM_SIZE} ${NUM_RUNS} ${OUT_DIR}
done