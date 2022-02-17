import matplotlib
from matplotlib import pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.patches import Patch
import numpy as np
import os
from matplotlib.pyplot import bar, figure
import json

if os.path.isdir("./results/evaluation/"):
    RESULTS_PATH = "./results/evaluation/"
else:
    RESULTS_PATH = "./results-paper/evaluation/"

colors=mcolors.CSS4_COLORS
in_monitor_color=colors["darkcyan"]
guest_boot_color=colors["deepskyblue"]
decompress_color=colors["mediumseagreen"]
bootstrap_color=colors["orchid"]
bar_color="white"

figure(figsize=(8, 3))

def eval():

    legend = [ 
        Patch(edgecolor=guest_boot_color, facecolor=bar_color, label="Linux Boot", hatch="///"),
        Patch(edgecolor=decompress_color, facecolor=bar_color, label="Decompression", hatch="XX"),
        Patch(edgecolor=bootstrap_color, facecolor=bar_color, label="Bootstrap Setup", hatch="\|\|"),
        Patch(edgecolor=in_monitor_color, facecolor=bar_color, label="In Monitor", hatch="\\\\\\"),
    ]

    legend.reverse()

    files = os.listdir(RESULTS_PATH)

    bzImage_fgkaslr_none={}
    bzImage_fgkaslr_lz4={}
    bzImage_kaslr_none={}
    bzImage_kaslr_lz4={}
    bzImage_nokaslr_none={}
    bzImage_nokaslr_lz4={}
    vmlinux_fgkaslr={}
    vmlinux_kaslr={}
    vmlinux_nokaslr={}


    for f in files:
        lines = open(RESULTS_PATH + f).readlines()
        f_tokens = f.split("-")
        name = f_tokens[1]
        total_times=[]
        decomp_times=[]
        in_monitor_times=[]
        guest_boot_times=[]
        bootstrap_times=[]
        parse_elf_times=[]
        bootstrap_rando_times=[]
        in_monitor_rando_times=[]
        components={}
        for l in lines:
            l = json.loads(l)
            total=0
            total += int(l["decomp"])/1000.0
            total += int(l["in_monitor"])/1000.0
            total += int(l["guest"])/1000.0
            total += int(l["bootstrap"])/1000.0
            total += int(l["parse_elf"])/1000.0
            total += int(l["bootstrap_rando"])/1000.0
            add = True
            for key in l:
                if int(l[key]) < 0:
                    add=False
                if int(l["guest"] <= 0):
                    add = False
            if add:
                total_times.append(total)    
                decomp_times.append(int(l["decomp"])/1000.0)
                in_monitor_times.append((int(l["in_monitor"])/1000.0))
                guest_boot_times.append(int(l["guest"])/1000.0)
                bootstrap_times.append(int(l["bootstrap"])/1000.0 + ((int(l["parse_elf"])/1000.0) if "fgkaslr" not in f else 0) +  (int(l["bootstrap_rando"])/1000.0) + ((int(l["parse_elf"])/1000.0) if "fgkaslr" in f else 0))
                in_monitor_rando_times.append(int(l["in_monitor_rando"])/1000.0)

        components["in_monitor"] = in_monitor_times
        components["bootstrap"] = bootstrap_times
        components["decomp"] = decomp_times
        components["bootstrap_rando"] = bootstrap_rando_times
        components["in_monitor_rando"] = in_monitor_rando_times
        components["guest"] = guest_boot_times
        components["total"] = total_times
        
        if "bzImage" in f:
            if "none" in f:
                if "nokaslr" in f:
                    bzImage_nokaslr_none[name] = (np.average(total_times), components)
                if "-kaslr" in f:
                    bzImage_kaslr_none[name] = (np.average(total_times), components)
                if "fgkaslr" in f:
                    bzImage_fgkaslr_none[name] = (np.average(total_times), components)
            if "lz4" in f:
                if "nokaslr" in f:
                    bzImage_nokaslr_lz4[name] = (np.average(total_times), components)
                if "-kaslr" in f:
                    bzImage_kaslr_lz4[name] = (np.average(total_times), components)
                if "fgkaslr" in f:
                    bzImage_fgkaslr_lz4[name] = (np.average(total_times), components)
        if "vmlinux" in f:
            if "nokaslr" in f:
                vmlinux_nokaslr[name] = (np.average(total_times), components)
            if "-kaslr" in f:
                vmlinux_kaslr[name] = (np.average(total_times), components)
            if "fgkaslr" in f:
                vmlinux_fgkaslr[name] = (np.average(total_times), components)
            
        all_dicts = [ 
            vmlinux_nokaslr, 
            bzImage_nokaslr_none,
            bzImage_nokaslr_lz4, 
            vmlinux_kaslr, 
            bzImage_kaslr_none,
            bzImage_kaslr_lz4, 
            vmlinux_fgkaslr, 
            bzImage_fgkaslr_none,
            bzImage_fgkaslr_lz4
        ]

    nokaslr = [all_dicts[0], all_dicts[1], all_dicts[2]]
    kaslr = [all_dicts[3], all_dicts[4], all_dicts[5]]
    fgkaslr = [all_dicts[6], all_dicts[7], all_dicts[8]]

    types = [nokaslr, kaslr, fgkaslr]
    bar_width = 0.27

    figure(figsize=(8,4.8))

    for kernel in ["lupine4", "aws", "ubuntu"]:

        x_ax = [1, 2.5, 4]

        for x, type in zip(x_ax, types):
            for t in type:
                comps=t[kernel][1]

                total = comps["total"]

                dev = np.max(total) - np.min(total)

                plt.bar(
                    x, 
                    np.average(comps["guest"]),
                    bottom = np.average(comps["decomp"]) + np.average(comps["bootstrap"]) + np.average(comps["in_monitor"]),
                    width=bar_width,
                    color=bar_color,
                    edgecolor=guest_boot_color,
                    hatch="///",
                    yerr=dev,
                    capsize=3
                )

                plt.bar(
                    x, 
                    np.average(comps["decomp"]),
                    bottom=np.average(comps["bootstrap"]) + np.average(comps["in_monitor"]),
                    width=bar_width,
                    color=bar_color,
                    edgecolor=decompress_color,
                    hatch="XX"
                )

                plt.bar(
                    x, 
                    np.average(comps["bootstrap"]),
                    bottom=np.average(comps["in_monitor"]),
                    width=bar_width,
                    color=bar_color,
                    edgecolor=bootstrap_color,
                    hatch="\|\|"
                )

                plt.bar(
                    x, 
                    np.average(comps["in_monitor"]),
                    bottom=None, 
                    width=bar_width,
                    color=bar_color,
                    edgecolor=in_monitor_color,
                    hatch="\\\\\\"
                )

                x += bar_width + 0.05

        title = kernel[0].capitalize() + kernel[1:]
        if title == "Aws":
            title = title.upper()
        if title == "Lupine4":
            title = "Lupine"

        ax = plt.gca()
        trans = ax.get_xaxis_transform() # x in data untis, y in axes fraction
        ax.annotate('No KASLR', xy=(1.3, 0.6 ), xycoords=trans, ha='center')
        ax.annotate('KASLR', xy=(2.8, 0.6 ), xycoords=trans, ha='center')
        ax.annotate('FG_KASLR', xy=(4.3, 0.9), xycoords=trans, ha='center')

        ax.set_ylim([ax.get_ylim()[0], ax.get_ylim()[1] * 1.1])
        plt.title(title)
        plt.legend(handles=legend)
        plt.xticks([1, 1.325, 1.65, 2.5, 2.825, 3.15, 4, 4.325, 4.65], [
            "Direct Boot",
            "Compression None",
            "LZ4",
            "Direct Boot",
            "Compression None",
            "LZ4",
            "Direct Boot",
            "Compression None",
            "LZ4",
        ], rotation=-25, ha='left')
        plt.ylabel("Time (ms)")
        plt.tight_layout()
        plt.savefig("./graphs/" + kernel + "-eval.pdf", format='pdf')
        plt.cla()

if __name__ == "__main__":  
    eval()