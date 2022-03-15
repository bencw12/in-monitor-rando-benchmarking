import matplotlib
from matplotlib import pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.patches import Patch
import numpy as np
import os
from matplotlib.pyplot import bar, figure
import json

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

if os.path.isdir("./results/bootstrap-comparison/"):
    RESULTS_PATH = "./results/bootstrap-comparison/"
else:
    RESULTS_PATH = "./results-paper/bootstrap-comparison/"

colors= mcolors.CSS4_COLORS
in_monitor_color=colors["darkcyan"]
guest_boot=colors["deepskyblue"]
decompress_color=colors["mediumseagreen"]
bar_color="white"
figure(figsize=(8,3.6))


def bootstrap_comparison():
    lines_width=2
    matplotlib.rcParams['hatch.linewidth'] = lines_width
    x_ax = [1, 1.2, 1.4, 1.6, 2, 2.2, 2.4, 2.6, 3, 3.2, 3.4, 3.6]
    bar_width=0.2

    x_labels = ["lupine-none", "lupine-lz4", "lupine-none-optimized", "lupine-uncompressed", "aws-none", "aws-lz4", "aws-none-optimized", "aws-uncompressed", "ubuntu-none", "ubuntu-lz4", "ubuntu-none-optimized", "ubuntu-uncompressed"]

    plt.xticks(x_ax, x_labels, rotation=-20, ha='left')

    k = [("bzImage-lupine4-nokaslr-none-cache.txt", "bzImage-lupine4-nokaslr-lz4-cache.txt", "bzImage-lupine4-nokaslr-none-optimized-cache.txt", "vmlinux-lupine4-nokaslr-cache.txt"),
        ("bzImage-aws-nokaslr-none-cache.txt", "bzImage-aws-nokaslr-lz4-cache.txt", "bzImage-aws-nokaslr-none-optimized-cache.txt", "vmlinux-aws-nokaslr-cache.txt"),
        ("bzImage-ubuntu-nokaslr-none-cache.txt", "bzImage-ubuntu-nokaslr-lz4-cache.txt", "bzImage-ubuntu-nokaslr-none-optimized-cache.txt", "vmlinux-ubuntu-nokaslr-cache.txt"),
       ]

    x_ax = [1, 2, 3]

    legend = [
        Patch(edgecolor=guest_boot, facecolor=bar_color, label="Linux Boot", hatch="\\\\\\"),
        Patch(edgecolor=decompress_color, facecolor=bar_color, label="Bootstrap Loader", hatch="..."),
        Patch(edgecolor=in_monitor_color, facecolor=bar_color, label="In-Monitor", hatch="///"),
    ]

    plt.legend(handles=legend)
    plt.ylabel("Time (ms)")

    for kernel, x in zip(k, x_ax):
        f_none, f_lz4, f_none_optimized, f_uncompressed = kernel

        with open(RESULTS_PATH + f_none) as f:
            lines = f.readlines()

            parse_elf_times = []
            decomp_times = []
            bootstrap_times = []
            in_monitor_times = []
            boot_times = []

            for l in lines:
                l = json.loads(l)
                in_monitor_times.append(l["in_monitor"]/1000.0)
                parse_elf_times.append(l["parse_elf"]/1000.0)
                decomp_times.append(l["decomp"]/1000.0)
                bootstrap_times.append(l["bootstrap"]/1000.0)
                boot_times.append(l["guest"]/1000.0)

            
            bootstrap_loader_time = np.average(bootstrap_times) + np.average(decomp_times) + np.average(parse_elf_times)
            max_bootstrap_loader_time = np.max(bootstrap_times) + np.max(decomp_times) + np.max(parse_elf_times)
            min_bootstrap_loader_time = np.min(bootstrap_times) + np.min(decomp_times) + np.min(parse_elf_times)

            plt.bar(x, np.average(boot_times), bottom=bootstrap_loader_time + np.average(in_monitor_times), width=bar_width, hatch="\\\\\\", edgecolor=guest_boot, color=bar_color, linewidth=lines_width, yerr=np.max(boot_times)-np.min(boot_times), capsize=lines_width*2)
            plt.bar(x, bootstrap_loader_time, bottom=np.average(in_monitor_times), width=bar_width, hatch="...", edgecolor=decompress_color, color=bar_color, linewidth=lines_width, yerr=max_bootstrap_loader_time-min_bootstrap_loader_time, capsize=lines_width*2)
            plt.bar(x, np.average(in_monitor_times), bottom=None, width=bar_width, hatch="///", edgecolor=in_monitor_color, color=bar_color, linewidth=lines_width, yerr=np.max(in_monitor_times)-np.min(in_monitor_times), capsize=lines_width*2)

        x += 0.2

        with open(RESULTS_PATH + f_lz4) as f:
            lines = f.readlines()

            parse_elf_times1 = []
            decomp_times1 = []
            bootstrap_times1 = []
            in_monitor_times = []
            boot_times = []

            for l in lines:
                l = json.loads(l)
                in_monitor_times.append(l["in_monitor"]/1000.0)
                parse_elf_times1.append(l["parse_elf"]/1000.0)
                decomp_times1.append(l["decomp"]/1000.0)
                bootstrap_times1.append(l["bootstrap"]/1000.0)
                boot_times.append(l["guest"]/1000.0)

            bootstrap_loader_time = np.average(bootstrap_times1) + np.average(decomp_times1) + np.average(parse_elf_times1)
            max_bootstrap_loader_time = np.max(bootstrap_times1) + np.max(decomp_times1) + np.max(parse_elf_times1)
            min_bootstrap_loader_time = np.min(bootstrap_times1) + np.min(decomp_times1) + np.min(parse_elf_times1)

            plt.bar(x, np.average(boot_times), bottom=bootstrap_loader_time + np.average(in_monitor_times), width=bar_width, hatch="\\\\\\", edgecolor=guest_boot, color=bar_color, linewidth=lines_width, yerr=np.max(boot_times)-np.min(boot_times), capsize=lines_width*2)
            plt.bar(x, bootstrap_loader_time, bottom=np.average(in_monitor_times), width=bar_width, hatch="...", edgecolor=decompress_color, color=bar_color, linewidth=lines_width, yerr=max_bootstrap_loader_time-min_bootstrap_loader_time, capsize=lines_width*2)
            plt.bar(x, np.average(in_monitor_times), bottom=None, width=bar_width, hatch="///", edgecolor=in_monitor_color, color=bar_color, linewidth=lines_width, yerr=np.max(in_monitor_times)-np.min(in_monitor_times), capsize=lines_width*2)
            x += 0.2

        with open(RESULTS_PATH + f_none_optimized) as f:
            lines = f.readlines()

            parse_elf_times1 = []
            decomp_times1 = []
            bootstrap_times1 = []
            in_monitor_times = []
            boot_times = []

            for l in lines:
                l = json.loads(l)
                in_monitor_times.append(l["in_monitor"]/1000.0)
                parse_elf_times1.append(l["parse_elf"]/1000.0)
                decomp_times1.append(l["decomp"]/1000.0)
                bootstrap_times1.append(l["bootstrap"]/1000.0)
                boot_times.append(l["guest"]/1000.0)

            bootstrap_loader_time = np.average(bootstrap_times1) + np.average(decomp_times1) + np.average(parse_elf_times1)
            max_bootstrap_loader_time = np.max(bootstrap_times1) + np.max(decomp_times1) + np.max(parse_elf_times1)
            min_bootstrap_loader_time = np.min(bootstrap_times1) + np.min(decomp_times1) + np.min(parse_elf_times1)

            plt.bar(x, np.average(boot_times), bottom=bootstrap_loader_time + np.average(in_monitor_times), width=bar_width, hatch="\\\\\\", edgecolor=guest_boot, color=bar_color, linewidth=lines_width, yerr=np.max(boot_times)-np.min(boot_times), capsize=lines_width*2)
            plt.bar(x, bootstrap_loader_time, bottom=np.average(in_monitor_times), width=bar_width, hatch="...", edgecolor=decompress_color, color=bar_color, linewidth=lines_width, yerr=max_bootstrap_loader_time-min_bootstrap_loader_time, capsize=lines_width*2)
            plt.bar(x, np.average(in_monitor_times), bottom=None, width=bar_width, hatch="///", edgecolor=in_monitor_color, color=bar_color, linewidth=lines_width, yerr=np.max(in_monitor_times)-np.min(in_monitor_times), capsize=lines_width*2)
            
        x += 0.2

        with open(RESULTS_PATH + f_uncompressed) as f:
            lines = f.readlines()

            parse_elf_times1 = []
            decomp_times1 = []
            bootstrap_times1 = []
            in_monitor_times = []
            boot_times = []

            for l in lines:
                l = json.loads(l)
                in_monitor_times.append(l["in_monitor"]/1000.0)
                parse_elf_times1.append(l["parse_elf"]/1000.0)
                decomp_times1.append(l["decomp"]/1000.0)
                bootstrap_times1.append(l["bootstrap"]/1000.0)
                boot_times.append(l["guest"]/1000.0)

            bootstrap_loader_time = np.average(bootstrap_times1) + np.average(decomp_times1) + np.average(parse_elf_times1)
            max_bootstrap_loader_time = np.max(bootstrap_times1) + np.max(decomp_times1) + np.max(parse_elf_times1)
            min_bootstrap_loader_time = np.min(bootstrap_times1) + np.min(decomp_times1) + np.min(parse_elf_times1)

            plt.bar(x, np.average(boot_times), bottom=bootstrap_loader_time + np.average(in_monitor_times), width=bar_width, hatch="\\\\\\", edgecolor=guest_boot, color=bar_color, linewidth=lines_width, yerr=np.max(boot_times)-np.min(boot_times), capsize=lines_width*2)
            plt.bar(x, np.average(in_monitor_times), bottom=None, width=bar_width, hatch="///", edgecolor=in_monitor_color, color=bar_color, linewidth=lines_width, yerr=np.max(in_monitor_times)-np.min(in_monitor_times), capsize=lines_width*2)


    plt.tight_layout()
    plt.savefig("./graphs/bootstrap-method-comparison.pdf", format="pdf")
    plt.cla()

if __name__ == "__main__":
    bootstrap_comparison()