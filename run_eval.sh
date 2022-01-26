#!/bin/bash
# Experiment for Figure 9

MEM_SIZE=256
CACHE_OPT=cache
OUT_DIR=./results/evaluation

if ! [[ ${1}  =~ ^[+-]?[0-9]+\.?[0-9]*$ ]]; then
    echo "Please enter the number of runs"
    exit 1
fi

mkdir -p ${OUT_DIR}

NUM_RUNS=${1}

for kernel in lupine4 aws ubuntu; do
    for kaslr_opt in nokaslr kaslr fgkaslr; do
        ./run_batch.sh ./kernels/uncompressed/vmlinux-${kernel}-${kaslr_opt} ${kaslr_opt} ${CACHE_OPT} ${MEM_SIZE} ${NUM_RUNS} ${OUT_DIR}

        if [ ${kaslr_opt} == fgkaslr ]; then
            kaslr_opt=fgkaslr-no-kallsyms
        fi

        ./run_batch.sh ./kernels/optimized-compression-none/bzImage-${kernel}-${kaslr_opt}-none-optimized bzImage ${CACHE_OPT} ${MEM_SIZE} ${NUM_RUNS} ${OUT_DIR}
        ./run_batch.sh ./kernels/lz4/bzImage-${kernel}-${kaslr_opt}-lz4 bzImage ${CACHE_OPT} ${MEM_SIZE} ${NUM_RUNS} ${OUT_DIR}
    done
done

