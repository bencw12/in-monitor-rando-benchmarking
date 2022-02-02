import matplotlib
from matplotlib import pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.patches import Patch
import numpy as np
import os
from matplotlib.pyplot import bar, figure
import json

if os.path.isdir("./results/mem-size/"):
    RESULTS_PATH = "./results/mem-size/"
else:
    RESULTS_PATH = "./results-paper/mem-size/"

colors=mcolors.CSS4_COLORS
bootstrap_color=colors["darkcyan"]
parse_elf_color=colors["deepskyblue"]
decompress_color=colors["mediumseagreen"]
rando_color=colors["darkorange"]
bar_color="white"

def mem_experiments():

    figure(figsize=(6,3))

    all_dirs = os.listdir(RESULTS_PATH)

    

    all_files = {}

    acc = 0
    for size in all_dirs:
        all_files[size] = os.listdir(RESULTS_PATH + all_dirs[acc])
        acc+=1

    lupine_nokaslr = {}
    lupine_kaslr = {}
    lupine_fgkaslr = {}
    aws_nokaslr = {}
    aws_kaslr = {}
    aws_fgkaslr = {}
    ubuntu_nokaslr = {}
    ubuntu_kaslr = {}
    ubuntu_fgkaslr = {}

    for size in all_dirs:
        for file in all_files[size]:
            if "aws" in file:
                if "fgkaslr" in file:
                    aws_fgkaslr[size] = file
                elif "nokaslr" in file:
                    aws_nokaslr[size] = file
                else:
                    aws_kaslr[size] = file
            if "lupine" in file:
                if "fgkaslr" in file:
                    lupine_fgkaslr[size] = file
                elif "nokaslr" in file:
                    lupine_nokaslr[size] = file
                else:
                    lupine_kaslr[size] = file
            if "ubuntu" in file:
                if "fgkaslr" in file:
                    ubuntu_fgkaslr[size] = file
                elif "nokaslr" in file:
                    ubuntu_nokaslr[size] = file
                else:
                    ubuntu_kaslr[size] = file


    all_bars = [lupine_nokaslr, lupine_kaslr, lupine_fgkaslr, aws_nokaslr, aws_kaslr, aws_fgkaslr, ubuntu_nokaslr, ubuntu_kaslr, ubuntu_fgkaslr]

    legend=[
        Patch(facecolor=decompress_color, label="256M"),
        Patch(facecolor=bootstrap_color, label="512M"),
        Patch(facecolor=parse_elf_color, label="1G"),
        Patch(facecolor=rando_color, label="2G"),
    ]

    plt.legend(handles=legend, ncol=4)


    results = {}
    keys = []

    x_ax= [0, 1, 2, 4, 5, 6, 8, 9, 10]
    colors= [decompress_color, bootstrap_color, parse_elf_color, rando_color]

    for bars, x in zip(all_bars, x_ax):

        for size_i in range(4):

            temp = bars[all_dirs[size_i]]
            f = open(RESULTS_PATH + all_dirs[size_i] + "/" + temp)
            f = f.readlines()

            in_monitor_times = []
            guest_times = []

            for line in f:
                line = json.loads(line)

                if int(line["guest"] > 0):
                    in
                    total_times.append(
                        (int(line["in_monitor"], int(line["guest"])))
                    )
                    

                total_times.append(total) 

            plt.bar(
                x + (0.2*size_i), 
                np.average(total_times)/1000.0,
                width=0.2,
                color=colors[size_i]
            )

    keys = ['lupine-nokaslr', 'lupine-kaslr', 'lupine-fgkaslr',
        'aws-nokaslr', 'aws-kaslr', 'aws-fgkaslr',
        'ubuntu-nokaslr', 'ubuntu-kaslr', 'ubuntu-fgkaslr']

    plt.xticks([i + 0.3 for i in x_ax], keys, rotation=-20, ha='left')

    plt.tight_layout()
    plt.savefig("./graphs/mem-experiments.pdf", format='pdf')     

mem_experiments()