#!/bin/bash

mkdir ./mount-boottime
mkdir ./mount-lebench
touch ./lebench.ext4

dd if=/dev/zero of=./lebench.ext4 bs=1M count=150
mkfs.ext4 ./lebench.ext4
e2fsck -fy ./lebench.ext4

mount -o loop ./boottime-rootfs.ext4 ./mount-boottime
mount -o loop ./lebench.ext4 ./mount-lebench

cp -r ./mount-boottime/* ./mount-lebench/
cp -r ./LEBench ./mount-lebench/
cp ./libc.so.6 ./mount-lebench/lib/
cp ./libpthread.so.0 ./mount-lebench/lib/

umount ./mount-lebench
umount ./mount-boottime

rm -rf ./mount-boottime
rm -rf ./mount-lebench
