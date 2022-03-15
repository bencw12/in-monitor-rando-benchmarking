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

if os.path.isdir("./results/cache-effects/"):
    RESULTS_PATH = "./results/cache-effects/"
else:
    RESULTS_PATH = "./results-paper/cache-effects/"

def bootstrap_breakdown():

    figure(figsize=(8,3.6))    
    lines=2
    matplotlib.rcParams['hatch.linewidth'] = lines
    new_kernels = [ "bzImage-lupine4-nokaslr-lz4-cache.txt", "bzImage-aws-nokaslr-lz4-cache.txt", "bzImage-ubuntu-nokaslr-lz4-cache.txt"]

    ax = [1, 1.5, 2]
    labels = ["lupine", "aws", "ubuntu"]
    bar_width = 0.15
    colors= mcolors.CSS4_COLORS
    bootstrap_color=colors["darkcyan"]
    parse_elf_color=colors["deepskyblue"]
    decompress_color=colors["mediumseagreen"]
    bar_color="white"

    legend = [
        Patch(edgecolor=parse_elf_color, facecolor=bar_color, label="parse_elf", hatch="\\\\\\"),
        Patch(edgecolor=decompress_color, facecolor=bar_color, label="decompression", hatch="..."),
        Patch(edgecolor=bootstrap_color, facecolor=bar_color, label="bootstrap setup", hatch="///"),
    ]

    decomp_percents = []

    for k, x in zip(new_kernels, ax):
        filename = RESULTS_PATH + k

        bootstrap_times = []
        decomp_times = []
        parse_elf_times = []
        handle_relocations_times = []
        post_relocations_times = []

        with open(filename) as f:
            all_json = f.readlines()

            for i in range(len(all_json)):
                try:
                    all_json[i]=json.loads(all_json[i])
                    bootstrap_times.append(all_json[i]["bootstrap"]/1000.0)
                    decomp_times.append(all_json[i]["decomp"]/1000.0)
                    parse_elf_times.append(all_json[i]["parse_elf"]/1000.0)
                except:
                    print(filename)

        bootstrap_time = np.average(bootstrap_times)
        bootstrap_min = np.min(bootstrap_times)
        bootstrap_max = np.max(bootstrap_times)
        decomp_time = np.average(decomp_times)
        decomp_min = np.min(decomp_times)
        decomp_max = np.max(decomp_times)
        parse_elf = np.average(parse_elf_times)
        parse_elf_min = np.min(parse_elf_times)
        parse_elf_max = np.max(parse_elf_times)

        decomp_percents.append(decomp_time/(bootstrap_time + decomp_time + parse_elf))
        
        plt.bar(x, parse_elf, width=bar_width, bottom=decomp_time + bootstrap_time, edgecolor=parse_elf_color, hatch="\\\\", color=bar_color, linewidth=lines, yerr=parse_elf_max-parse_elf_min, capsize=lines*2)
        plt.bar(x, decomp_time, width=bar_width, bottom=bootstrap_time, edgecolor=decompress_color, hatch="..", color=bar_color, linewidth=lines, yerr=decomp_max-decomp_min, capsize=lines*2)
        plt.bar(x, bootstrap_time, width=bar_width, bottom=None, edgecolor=bootstrap_color, hatch="//", color=bar_color, linewidth=lines, yerr=bootstrap_max-bootstrap_min, capsize=lines*2)
        
    plt.ylabel("Time (ms)")
    plt.xticks(ax, labels)
    plt.legend(handles=legend)
    plt.savefig("./graphs/bootstrap-loader-breakdown.pdf", format="pdf")
    plt.cla()

if __name__ == "__main__":
    bootstrap_breakdown()