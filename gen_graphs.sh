#!/bin/bash

rm -f ./graphs/*

for FILE in ./scripts/*; do
    python3 ${FILE} > /dev/null 2>&1
done
