#!/bin/bash

CACHE_OPT=cache

if ! [[ ${1}  =~ ^[+-]?[0-9]+\.?[0-9]*$ ]]; then
    echo "Please enter the number of runs"
    exit 1
fi

NUM_RUNS=${1}

mkdir -p ./results/mem-size/

for MEM_ALLOC in 256 512 1024 2048; do
    echo "${MEM_ALLOC}: "
    for kernel in lupine4 aws ubuntu; do
        for kaslr_opt in nokaslr kaslr fgkaslr; do
            OUT_DIR=./results/mem-size/${MEM_ALLOC}
            mkdir -p ${OUT_DIR}
            
            ./run_batch.sh ./kernels/uncompressed/vmlinux-${kernel}-${kaslr_opt} ${kaslr_opt} ${CACHE_OPT} ${MEM_ALLOC} ${NUM_RUNS} ${OUT_DIR}
        done
    done
done