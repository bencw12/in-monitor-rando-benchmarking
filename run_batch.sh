#!/bin/bash

# Arg checks
if [ "$#" -ne 6 ]; then
    echo "usage: $0 <kernel-path> [no][fg]kaslr/bzImage cache/no-cache <mem-alloc-mb> <num-runs> <output-dir>"
    exit 1
fi

if ! [ -f "${1}" ]; then
    echo "Kernel not found"
    exit 1
fi

if ! [ -d "${6}" ]; then
    echo "Output dir not found"
    exit 1
fi

if ! [[ "$2" =~ ^(nokaslr|kaslr|fgkaslr|bzImage)$ ]]; then
    echo "Need to specify nokaslr, kaslr, fgkaslr, or bzImage"
    exit 1
fi

if ! [[ $3 =~ ^(cache|no-cache)$ ]]; then
    echo "Enter 'cache' or 'no-cache'"
fi

if ! [[ $4 =~ ^[0-9]+$ ]]; then
    echo "Invalid amount of allocated memory"
    exit 1
fi

if ! [[ $5 =~ ^[0-9]+$ ]]; then
    echo "Invalid number of runs"
    exit 1
fi 
KERNEL_NAME=$(basename ${1})

# firecracker-nokaslr/firecracker-kaslr/firecracker-fgkaslr/firecracker-bzImage
bin=./bin/firecracker-${2}
outfile="${6}/${KERNEL_NAME}-${3}.txt"

# clear old results
rm -f ${outfile}

# warm up the cache if using it
if [ "${3}" = "cache" ]; then
    
    for ((n=0;n<5;n++)); do
	echo -ne "Warming cache $((n+1))/5\r"
        ${PWD}/run_benchmark.sh ${1} ${bin} ${3} ${4} > /dev/null 2>&1
    done
    echo ""
fi

for ((n=1;n<=$5;n++)); do
    echo -ne "${KERNEL_NAME} : ${n}/${5}\r"
    ${PWD}/run_benchmark.sh ${1} ${bin} $3 $4 >> ${outfile}
done
echo ""
exit 0
