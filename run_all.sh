#!/bin/bash
# Script to run all experiments

if ! [[ ${1}  =~ ^[+-]?[0-9]+\.?[0-9]*$ ]]; then
    echo "Please enter the number of runs for each experiment"
    exit 1
fi

echo "Running compression bakeoff: "

./run_compression_bakeoff.sh ${1}

echo "Running cache effects bakeoff: "

./run_cache_effects.sh ${1}

echo "Running bootstrap comparison: "

./run_bootstrap_comparison.sh ${1}

echo "Running evaluation: "

./run_eval.sh ${1}

echo "Running guest memory experiments: "

./run_mem_size.sh ${1}

echo "Running LEBench experiments: "

./run_lebench.sh