#!/bin/bash

# Arg checks
if [ "$#" -ne 1 ]; then
    echo "usage: $0 <nokaslr/kaslr/fgkaslr>"
    exit 1
fi

if ! [[ $1 =~ ^(nokaslr|kaslr|fgkaslr)$ ]]; then
    echo "Enter nokaslr, kaslr, or fgkaslr."
    exit 1
fi

if [[ $1 =~ ^(kaslr|fgkaslr)$ ]]; then
    RELOCS_OPT=", 
    \"relocs_path\": \"${PWD}/relocs/vmlinux-aws-${1}.relocs\""
else
    RELOCS_OPT=""
fi

KERNEL_PATH=./kernels/uncompressed/vmlinux-aws-${1}
FC_BIN=./bin/firecracker-${1}
ROOTFS_PATH=./rootfs/lebench.ext4

mkdir -p ./results/lebench

RUNNER="#!/bin/ash"$'\n'"cd /LEBench/TEST_DIR"$'\n'"export LEBENCH_DIR=\"/LEBench/\""$'\n'"./OS_Eval 0 ${1}"$'\n'"reboot"

echo "$RUNNER" > ./rootfs/LEBench/run.sh
chmod +x ./rootfs/LEBench/run.sh

cd ./rootfs
./mk-lebench-rootfs.sh
cd ../

BOOT_ARGS="reboot=k panic=1 pci=off console=ttyS0"
CONFIG_FILE="{
                    \"boot-source\": {
                        \"kernel_image_path\": \"${KERNEL_PATH}\",
                        \"boot_args\": \"${BOOT_ARGS}\"${RELOCS_OPT}
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
                        \"mem_size_mib\": 256,
                        \"ht_enabled\": false,
                        \"track_dirty_pages\": false
                    }
                }"

echo ${CONFIG_FILE} > ./vm_config.json

rm -rf /tmp/firecracker.socket

${FC_BIN}   --api-sock /tmp/firecracker.socket --no-api --config-file ./vm_config.json

mkdir -p ./rootfs/mount
mount -o loop ./rootfs/lebench.ext4 ./rootfs/mount
cp ./rootfs/mount/LEBench/output.${1}.csv ./results/lebench/
umount ./rootfs/mount
rm -rf ./rootfs/mount