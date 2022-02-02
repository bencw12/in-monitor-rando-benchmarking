import matplotlib
from matplotlib import pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.patches import Patch
import numpy as np
import os
from matplotlib.pyplot import bar, figure
import json

if os.path.isdir("./results/cache-effects/"):
    RESULTS_PATH = "./results/cache-effects/"
else:
    RESULTS_PATH = "./results-paper/cache-effects/"

colors=mcolors.CSS4_COLORS
in_monitor_color=colors["darkcyan"]
bootstrap_color=colors["deepskyblue"]
guest_color=colors["mediumseagreen"]
bar_color="white"

def cache_effects():

    figure(figsize=(8,3.6))
    files=os.listdir(RESULTS_PATH)

    cache={
        "lupine" : [],
        "aws" : [],
        "ubuntu" : []
    }

    no_cache={
        "lupine" : [],
        "aws" : [],
        "ubuntu" : []
    }

    for f in files:
        if "no-cache" in f:
            if "lupine" in f:
                no_cache["lupine"].append(f)
            if "aws" in f:
                no_cache["aws"].append(f)
            if "ubuntu" in f:
                no_cache["ubuntu"].append(f)
        else:
            if "lupine" in f:
                cache["lupine"].append(f)
            if "aws" in f:
                cache["aws"].append(f)
            if "ubuntu" in f:
                cache["ubuntu"].append(f)

    k = [
        sorted(no_cache["lupine"], reverse=True),
        sorted(no_cache["aws"], reverse=True),
        sorted(no_cache["ubuntu"], reverse=True),
        sorted(cache["lupine"], reverse=True),
        sorted(cache["aws"], reverse=True),
        sorted(cache["ubuntu"], reverse=True)
    ]
    
    
    x_ax = [1, 2.2, 3.4, 4.6, 5.8, 7]
    bar_width = 0.3
    bar_color="white"
    line_width=2
    x_labels = ["lupine-vmlinux", "lupine-bzImage", "aws-vmlinux", "aws-bzImage",
                "ubuntu-vmlinux", "ubuntu-bzImage","lupine-vmlinux", "lupine-bzImage", "aws-vmlinux", "aws-bzImage",
                "ubuntu-vmlinux", "ubuntu-bzImage"]
    x_ticks = [1, 1.34, 2.2, 2.54, 3.4, 3.74, 4.6, 4.94, 5.8, 6.14, 7, 7.34]

    plt.ylabel("Time (ms)")
    plt.xticks(x_ticks, x_labels, rotation=-25, ha='left')

    for kernel, x in zip(k, x_ax):

        f_direct, f_compressed = kernel
    
        with open(RESULTS_PATH + f_direct) as f:
            in_monitor_times = []
            bootstrap_times = []
            decomp_times = []
            parse_elf_times = []
            boot_times = []
            lines = f.readlines()
            for l in lines:
                l = json.loads(l)
                in_monitor_times.append(l["in_monitor"]/1000.0)
                bootstrap_times.append(l["bootstrap"]/1000.0)
                decomp_times.append(l["decomp"]/1000.0)
                parse_elf_times.append(l["parse_elf"]/1000.0)
                boot_times.append(l["guest"]/1000.0)

            max_total = np.max(boot_times) + np.max(in_monitor_times)
            min_total = np.min(boot_times) + np.min(in_monitor_times)

            plt.bar(x, np.average(boot_times), capsize=4, yerr=max_total-min_total, width=bar_width, bottom=np.average(in_monitor_times), color=bar_color, linewidth=line_width, hatch="\\\\\\", edgecolor=guest_color)
            plt.bar(x, np.average(in_monitor_times), width=bar_width, bottom=None, color=bar_color, linewidth=line_width, edgecolor=in_monitor_color, hatch="///")

        with open(RESULTS_PATH + f_compressed) as f:
            in_monitor_times = []
            bootstrap_times = []
            decomp_times = []
            parse_elf_times = []
            boot_times = []
            lines = f.readlines()
            for l in lines:
                l = json.loads(l)
                in_monitor_times.append(l["in_monitor"]/1000.0)
                bootstrap_times.append(l["bootstrap"]/1000.0)
                decomp_times.append(l["decomp"]/1000.0)
                parse_elf_times.append(l["parse_elf"]/1000.0)
                boot_times.append(l["guest"]/1000.0)

            bootstrap_loader_time = np.average(parse_elf_times) + np.average(decomp_times) + np.average(bootstrap_times)
            max_bootstrap_loader_time = np.max(parse_elf_times) + np.max(decomp_times) + np.max(bootstrap_times)
            min_bootstrap_loader_time = np.min(parse_elf_times) + np.min(decomp_times) + np.min(bootstrap_times)

            max_total = max_bootstrap_loader_time + np.max(in_monitor_times) + np.max(boot_times)
            min_total = min_bootstrap_loader_time + np.min(in_monitor_times) + np.min(boot_times)

            plt.bar(x + 0.34, np.average(boot_times), yerr=max_total-min_total, capsize=4,  width=bar_width, bottom=np.average(in_monitor_times) + bootstrap_loader_time, color=bar_color, edgecolor=guest_color, linewidth=line_width, hatch="\\\\\\")
            plt.bar(x + 0.34, bootstrap_loader_time, width=bar_width, bottom=np.average(in_monitor_times),color= bar_color, edgecolor=bootstrap_color, linewidth=line_width, hatch="...")
            plt.bar(x + 0.34, np.average(in_monitor_times), width=bar_width, bottom=None, color=bar_color, edgecolor=in_monitor_color, linewidth=line_width, hatch="///")

    legend_elements = [
        Patch(edgecolor=in_monitor_color, facecolor=bar_color, hatch="///" ,label="In-Monitor"),
        Patch(edgecolor=bootstrap_color, facecolor=bar_color, hatch="..." ,label="Boostrap Loader"),
        Patch(edgecolor=guest_color, facecolor=bar_color, hatch="\\\\\\" ,label="Linux Boot"),
    ]
    ax = plt.gca()
    transform = ax.get_xaxis_transform()
    ann = ax.annotate('No Cache', xy=(2.35, 0.6 ), xycoords=transform, ha="center")
    ann = ax.annotate('Cached', xy=(5.9, 0.6 ), xycoords=transform, ha="center")
    plt.vlines(4.25, 0, 250, colors=["black"])
    plt.ylim(0, 250)
    plt.legend(handles=legend_elements)
    plt.tight_layout()
    plt.savefig("./graphs/overall-boot-breakdown.pdf", format="pdf")

cache_effects()