#!/bin/bash

# Arg checks
if [ "$#" -ne 4 ]; then
    echo "usage: $0 <kernel-path> <firecracker-path> <cache/no-cache> <mem-alloc-mb>"
    exit 1
fi

if ! [ -f "${1}" ]; then
    echo "Kernel not found"
    exit 1
fi

FC_BIN="${2}"

if ! [ -f "${FC_BIN}" ]; then
    echo "Firecracker binary not found"
    exit 1
fi

if ! [[ $3 =~ ^(cache|no-cache)$ ]]; then
    echo "Enter 'cache' or 'no-cache'"
    exit 1
fi

if ! [[ $4 =~ ^[0-9]+$ ]]; then
    echo "Invalid amount of allocated memory"
    exit 1
fi

if [ "${3}" = "no-cache" ]; then
        sync; echo 3 > /proc/sys/vm/drop_caches
fi

ROOTFS_PATH=${PWD}/rootfs/lebench.ext4
KERNEL_NAME=$(basename ${1})

if ! [ -f "${ROOTFS_PATH}" ]; then
    echo "rootfs not found"
    exit 1
fi


if [[ $(basename ${2}) =~ ^(firecracker-kaslr|firecracker-fgkaslr)$ ]]; then
    RELOCS_PATH=${PWD}/relocs/${KERNEL_NAME}.relocs
    if ! [ -f "${RELOCS_PATH}" ]; then
        echo "Relocs not found"
        exit 1
    fi 
fi

BOOT_ARGS="reboot=k panic=1 pci=off nomodules 8250.nr_uarts=0 i8042.noaux i8042.nomux i8042.nopnp i8042.dumbkbd init=/sbin/fc_init"
if [[ $(basename ${2}) =~ ^(firecracker-nokaslr|firecracker-bzImage)$ ]]; then
    # Don't need relocs with bzImage or nokaslr
    CONFIG_FILE="{
                    \"boot-source\": {
                        \"kernel_image_path\": \"${1}\",
                        \"boot_args\": \"${BOOT_ARGS}\"
                    },
                    \"drives\": [
                        {
                        \"drive_id\": \"rootfs\",
                        \"path_on_host\": \"${ROOTFS_PATH}\",
                        \"is_root_device\": true,
                        \"is_read_only\": false
                        }
                    ],
                    \"machine-config\": {
                        \"vcpu_count\": 1,
                        \"mem_size_mib\": ${4},
                        \"ht_enabled\": false,
                        \"track_dirty_pages\": false
                    }
                }"
else   
    CONFIG_FILE="{
                    \"boot-source\": {
                        \"kernel_image_path\": \"${1}\",
                        \"boot_args\": \"${BOOT_ARGS}\",
                        \"relocs_path\": \"${RELOCS_PATH}\"
                    },
                    \"drives\": [
                        {
                        \"drive_id\": \"rootfs\",
                        \"path_on_host\": \"${ROOTFS_PATH}\",
                        \"is_root_device\": true,
                        \"is_read_only\": false
                        }
                    ],
                    \"machine-config\": {
                        \"vcpu_count\": 1,
                        \"mem_size_mib\": ${4},
                        \"ht_enabled\": false,
                        \"track_dirty_pages\": false
                    }
                }"
fi

echo ${CONFIG_FILE} > ./vm_config.json

rm -f /tmp/logs.file
touch /tmp/logs.file
rm -rf /tmp/firecracker.socket

PERF="${PWD}/bin/perf"
PERF_DATA="/tmp/fc_perf.data"

#run perf in the background to record events
${PERF}     record -a -e kvm:kvm_pio -e sched:sched_process_exec -o ${PERF_DATA} > /dev/null 2>&1 &

PERF_PID=$! &> /dev/null
#give perf time to start
sleep 1

#start firecracker
${FC_BIN}   --api-sock /tmp/firecracker.socket --no-api --config-file ./vm_config.json --log-path /tmp/logs.file --level Debug --boot-timer

sleep 1

pkill perf &> /dev/null

sleep 1

mkdir -p ./perf/

#dump everything perf captured to file
${PERF} script -i ${PERF_DATA} > ${PWD}/perf/perf.log

#scape output for timing info

fc_exec=$(grep "${2}" ${PWD}/perf/perf.log | awk '{print $4}' | sed 's/\.//' | sed 's/://g' )

bootstrap_start=$(grep "at 0xf4" ${PWD}/perf/perf.log | grep "val 0x1 " | awk '{print $5}' |  sed 's/\.//g' | sed 's/://g' )
bootstrap_end=$(grep "at 0xf4" ${PWD}/perf/perf.log | grep "val 0x2 " | awk '{print $5}' |  sed 's/\.//g' | sed 's/://g'  )
extract_kernel_start=$(grep "at 0xf4" ${PWD}/perf/perf.log | grep "val 0x3 " | awk '{print $5}' |  sed 's/\.//g' | sed 's/://g' )
choose_random_loc_start=$(grep "at 0xf4" ${PWD}/perf/perf.log | grep "val 0x4 " | awk '{print $5}' |  sed 's/\.//g' | sed 's/://g' )
choose_random_loc_end=$(grep "at 0xf4" ${PWD}/perf/perf.log | grep "val 0x5 " | awk '{print $5}' |  sed 's/\.//g' | sed 's/://g' )
decomp_start=$(grep "at 0xf4" ${PWD}/perf/perf.log | grep "val 0x6 " | awk '{print $5}' |  sed 's/\.//g' | sed 's/://g' )
decomp_end=$(grep "at 0xf4" ${PWD}/perf/perf.log | grep "val 0x7 " | awk '{print $5}' |  sed 's/\.//g' | sed 's/://g' )
parse_elf_start=$(grep "at 0xf4" ${PWD}/perf/perf.log | grep "val 0x8 " | awk '{print $5}' |  sed 's/\.//g' | sed 's/://g' )
parse_elf_end=$(grep "at 0xf4" ${PWD}/perf/perf.log | grep "val 0x9 " | awk '{print $5}' |  sed 's/\.//g' | sed 's/://g' )
pre_relocs_start=$(grep "at 0xf4" ${PWD}/perf/perf.log | grep "val 0xa " | awk '{print $5}' |  sed 's/\.//g' | sed 's/://g' )
pre_relocs_end=$(grep "at 0xf4" ${PWD}/perf/perf.log | grep "val 0xb " | awk '{print $5}' |  sed 's/\.//g' | sed 's/://g' )
relocs_start=$(grep "at 0xf4" ${PWD}/perf/perf.log | grep "val 0xc " | awk '{print $5}' |  sed 's/\.//g' | sed 's/://g' )
relocs_end=$(grep "at 0xf4" ${PWD}/perf/perf.log | grep "val 0xd " | awk '{print $5}' |  sed 's/\.//g' | sed 's/://g' )
post_relocs_start=$(grep "at 0xf4" ${PWD}/perf/perf.log | grep "val 0xe " | awk '{print $5}' |  sed 's/\.//g' | sed 's/://g' )
post_relocs_end=$(grep "at 0xf4" ${PWD}/perf/perf.log | grep "val 0xf " | awk '{print $5}' |  sed 's/\.//g' | sed 's/://g' )
extract_kernel_end=$(grep "at 0xf4" ${PWD}/perf/perf.log | grep "val 0x10 " | awk '{print $5}' |  sed 's/\.//g' | sed 's/://g' )
boot_start=$(grep "at 0xf4" ${PWD}/perf/perf.log | grep "val 0x11 " | awk '{print $5}' |  sed 's/\.//g' | sed 's/://g' )
boot_end=$(grep "at 0xf4" ${PWD}/perf/perf.log | grep "val 0x12 " | awk '{print $5}' |  sed 's/\.//g' | sed 's/://g' )

if [ ${2} == "firecracker-bzImage" ]; then
    in_monitor=$((bootstrap_start-fc_exec))
else
    in_monitor=$((boot_start-fc_exec))
fi
guest=$((boot_end-boot_start))
parse_elf=$((parse_elf_end-parse_elf_start))
decomp=$((decomp_end-decomp_start))
bootstrap=$((bootstrap_end-bootstrap_start))
choose_random_loc=$((choose_random_loc_end-choose_random_loc_start))
pre_relocs=$((pre_relocs_end-pre_relocs_start))
relocs=$((relocs_end-relocs_start))
post_relocs=$((post_relocs_end-post_relocs_start))
bootstrap_rando=$((pre_relocs+relocs+post_relocs+choose_random_loc))

if ! [[ $bootstrap_rando  =~ ^[+-]?[0-9]+\.?[0-9]*$ ]]; then
        bootstrap_rando=0
fi

if [ "${bootstrap}" -lt "0" ]; then
    bootstrap=0
fi

echo "{\"in_monitor\" : ${in_monitor}, \"guest\" : ${guest}, \"bootstrap\" : ${bootstrap}, \"decomp\" : ${decomp}, \"parse_elf\" : ${parse_elf}, \"bootstrap_rando\" : ${bootstrap_rando}}"

