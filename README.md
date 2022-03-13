# In-Monitor (FG)KASLR Benchmarking Suite
This repository contains the scripts/kernels/binaries necessary to evaluate the performance of our implementation of in-monitor (FG)KASLR in Firecracker v0.26. We leverage `perf` (Linux profiling with performance counters), and small patches to the Linux kernel to make IO writes to a unique port to signal the beginning/end of relevant function calls/events. The first timestamp is taken when Firecracker is executed, and the last is taken after the call to execute the guest's `init` process. The results from the experiments we ran on our machine are also included. `perf` records and timestamps the call to exec Firecracker and each of the subsequent IO writes from the guest kernel.
## Machine Specs
- CPU: Intel(R) Core(TM) i7-4790 @ 3.60GHz
- Memory: 8GB DDR3 @ 1600MHz
- Storage: Crucial MX500 250GB SSD, 560mb/s reads 

## Dependencies
- `perf` depends on `libpython2.7`
- Firecracker recommends Linux 4.14, or 5.10
- Firecracker requires Intel/AMD x86_64 CPUs that offer hardware virtualization support
- Scripts to generate graphs need Python 3 and `python3-matplotlib`.

# Running Benchmarks

## Setup
Firecracker requires KVM access which can be granted
with: `sudo setfacl -m u:$USER:rw /dev/kvm`

## Experiments

`run_compression_bakeoff.sh <num-runs>` runs the experiment for [Figure 3](./graphs/compression-bakeoff.pdf) comparing overall boot time of bzImages using various compression schemes supported by Linux. The cache is warmed up before recording data for each kernel. Our results show that `lz4` is the fastest compression scheme.

`run_cache_effects.sh <num-runs>` runs the experiment for [Figure 4](./graphs/overall-boot-breakdown.pdf) and data used in [Figure 5](./graphs/bootstrap-loader-breakdown.pdf) to compare the affects of a warm/cold cache on boot time. Our results show that when kernels can be cached, booting an uncompressed kernel is optimal, and when the cache is cold, a bzImage achieves optimal performance.

:warning: **Depending on your machine's hardeware/software stack, results for Figure 4 may differ**: on our machine, booting a bzImage is faster than a direct boot when kernels aren't cached, but a machine with a faster storage device may result in a bzImage booting slower both when it is cached, and when it is not in the cache.  


`run_bootstrap_comparison.sh <num-runs>` runs the experiment for [Figure 6](./graphs/compression-none-vs-lz4-overall.pdf) comparing boot performance of [compression-none](https://github.com/bencw12/linux/tree/compression-none-old), bzImage with lz4 compression, [optimized-compression-none](https://github.com/bencw12/linux/tree/compression-none), and an uncompressed boot.

`run_eval.sh <num-runs>` runs the experiment for Figure 9 [a](./graphs/lupine4-eval.pdf), [b](./graphs/aws-eval.pdf) and [c](./graphs/ubuntu-eval.pdf) used to compare in-monitor randomization, self-randomization with optimized compression-none, and self-randomization with lz4 compression. Our results show that in-monitor is the fastest method of randomization, followed by compression-none, then lz4. 

`run_batch.sh <kernel-path> [no][fg]kaslr/bzImage cache/no-cache <mem-alloc-mb> <num-runs> <output-dir>` boots a kernel `num-runs` times and writes the output to `<kernel-name>-<cache/no-cache>.txt`. If given `cache` the cache is warmed by booting the kernel 5 times before recording data. Called by all of the above scripts.

`run_benchmark.sh <kernel-path> <firecracker-path> <cache/no-cache> <mem-alloc-mb>` boots a kernel with the specified Firecracker binary and outputs measurements from one boot to the terminal. If given `no-cache` caches are dropped before boot. Called by `run_batch.sh`

`run_lebench.sh` boots the `AWS` kernel with nokaslr, or in-monitor (FG)KASLR, with a rootfs containing the source for [LEBench](https://github.com/LinuxPerfStudy/LEBench) to evaluate kernel performance. This will boot the kernel, run LEBench, shutdown the kernel, and save the results a total of three times, once for each variant `nokaslr`/`kaslr`/`fgkaslr`.

`run_mem_size.sh <num-runs>` runs each uncompressed kernel with `nokaslr`, `kaslr`, and `fgkaslr` with 256M, 512M, 1024M, and 2048M of allocated memory to determine whether our implementation of in-monitor randomization is affected by the amount of memory given to a VM instance. Our results show that the time spent in-monitor does not change with respect to allocated memory, and that the time to execute the kernel increases as allocated memory increases, but in-monitor randomization does not affect this trend. The results for this experiment were not added to the paper, but we have included a script to generate a Figure displaying the results of this experiment as well.

`gen_graphs.sh` calls all the python scripts in ./scripts to generate graphs from the data in ./results-paper

## /bin
Contains 4 Firecracker binaries: the stock Firecracker without our patches [firecracker-nokaslr](https://github.com/bencw12/firecracker/tree/stock), Firecracker with just KASLR implemented: https://github.com/bencw12/firecracker/tree/kaslr, Firecracker with FG-KASLR implemented: https://github.com/bencw12/firecracker/tree/fgkaslr, and Firecracker with a patch based on [this pull request](https://github.com/firecracker-microvm/firecracker/pull/670) to boot a bzImage [firecracker-bzImage](https://github.com/bencw12/firecracker/tree/bzImage). The `perf` binary we used is also included.

To build any of the Firecracker binaries, run `tools/devtool build --release` from the root of the repository. To build `perf`, run `make` from `linux/tools/perf` in the Linux source tree.  
## /configs
Contains the Linux kernel configuration files for [Lupine](https://systems-seminar-uiuc.github.io/spring20/content/a-linux-in-unikernel-clothing.pdf), [AWS](https://github.com/bencw12/firecracker/blob/stock/resources/microvm-kernel-x86_64.config), and the config from the distribution of Ubuntu on our machine. For each kernel, there are three variants: `nokaslr`, with randomization disabled, `kaslr`, with just coarse-grained randomization, and `fgkaslr`, with fine-grained randomization. Note that the variants for different compression schemes are not included, but another scheme can be selected by commenting `CONFIG_KERNEL_GZIP` and enabling another compression option. Each of the configs were generated from Linux 5.11-rc3 with our [compression none](https://github.com/bencw12/linux/tree/compression-none) scheme, so each contains the `CONFIG_KERNEL_NONE` option.
## /kernels
Each kernel was compiled with IO writes with unique values before and after portions of the boot which are traced by `perf` so we can measure different parts of the boot process. Kernels with FG-KASLR implement these [patches](https://github.com/kaccardi/linux/tree/fg-kaslr) and are compiled without the fixup of `kallsyms` from this [tree](https://github.com/bencw12/linux/tree/perf-timestamps-fgkaslr-no-kallsyms). Kernels with `nokaslr` or `kaslr`
are built from a [tree](https://github.com/bencw12/linux/tree/perf-timestamps-kaslr) with the IO writes and without the FG-KASLR patches. All patches were implemented on top of the source tree for Linux version 5.11-rc3.


To boot your own kernel with our modified versions of Firecracker, the kernel configuration must enable KASLR (CONFIG_RANDOMIZE_BASE) or FG-KASLR (CONFIG_FG_KASLR) from the [FG-KASLR source tree](https://github.com/kaccardi/linux/tree/fg-kaslr). After building the kernel, the relocations can be obtained from `linux/arch/x86/boot/compressed/vmlinux.relocs` and provided to the VMM via the `relocs_path` configuration option.
### /compression-bakeoff
bzImages compressed with bzip2, gzip, lz4, lzma, lzo, and xz used to evaluate overall performance of each compression scheme during boot. 
### /compression-none
Kernels with the [first version of compression none](https://github.com/bencw12/linux/tree/compression-none-old) where, during what is normally decompression, the uncompressed kernel is copied from where it was loaded to where it will be run.
### /compression-none-optimized
Kernels with [optimized compression none](https://github.com/bencw12/linux/tree/compression-none) where the uncompressed kernel is linked to the bootstrap loader and aligned at `MIN_KERNEL_ALIGN` so that it can be executed from the location it was loaded into memory. Before decompression, we remove the relocation of the uncompressed kernel to where it would be safe for decompression, then, instead of decompressing the kernel, the pointer to the output buffer for decompression is redirected to the head of the uncompressed kernel.
### /lz4
Kernels compressed with lz4
### /uncompressed
The statically linked, stripped Linux kernel ELF taken from `arch/boot/compressed/vmlinux.bin` after kernel compilation.
## /relocs
Relocation information for each of the uncompressed kernels that implement KASLR or FG-KASLR, named according to `vmlinux-<lupine4/aws/ubuntu>-<kaslr/fgkaslr>.relocs`.
## /scripts
Python scripts to generate the graphs used in the paper.

## /results-paper
Data used to generate the graphs in the paper. Each experiment, except for memory experiments, booted all kernels with 256M
of allocated memory.

## /graphs
Output directory for generated graphs
