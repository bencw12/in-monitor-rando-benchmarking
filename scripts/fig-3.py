import matplotlib
from matplotlib import pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.patches import Patch
import numpy as np
import os
from matplotlib.pyplot import bar, figure
import json

if os.path.isdir("./results/compression-bakeoff/"):
    RESULTS_PATH = "./results/compression-bakeoff/"
else:
    RESULTS_PATH = "./results-paper/compression-bakeoff/"
    
colors=mcolors.CSS4_COLORS
ubuntu_color=colors["darkcyan"]
lupine_color=colors["deepskyblue"]
aws_color=colors["mediumseagreen"]
bar_color="white"

def compression_bakeoff():

    figure(figsize=(8, 3))

    legend = [
        Patch(edgecolor=lupine_color, facecolor=bar_color, label="Lupine", hatch="\\\\\\"),
        Patch(edgecolor=aws_color, facecolor=bar_color, label="AWS", hatch="..."),
        Patch(edgecolor=ubuntu_color, facecolor=bar_color, label="Ubuntu", hatch="///"),
    ]

    files = os.listdir(RESULTS_PATH)
    files.sort()

    lupine=[]
    aws=[]
    ubuntu=[]

    for f in files:
        if "lupine" in f:
            lupine.append(f)
        if "aws" in f:
            aws.append(f)
        if "ubuntu" in f:
            ubuntu.append(f)

    all = [(lupine, "lupine"), (aws, "aws"), (ubuntu, "ubuntu")]
    totals_dict = {}
    schemes = set()
    for arr, name in all:
        dict_obj = {}
        for f in arr:
            tokens = f.split("-")
            comp_scheme = tokens[3]
            schemes.add(comp_scheme)

            f = open(RESULTS_PATH + f)
            lines = f.readlines()
            totals=[]
            for x in lines:
                x = json.loads(x)
                total = 0
                for key in x:
                    total += x[key]
                totals.append(total)
            dict_obj[comp_scheme] = totals
        totals_dict[name]=dict_obj

    ordered_comp_schemes = []
    average_overall = []
    for x in schemes:
        aws_av = np.average(totals_dict["aws"][x])
        lupine_av = np.average(totals_dict["lupine"][x])
        ubuntu_av = np.average(totals_dict["ubuntu"][x])

        total_av = (aws_av + lupine_av + ubuntu_av)/3.0
        average_overall.append((x, total_av))

    average_overall.sort(key= lambda x: x[1])

    for x in average_overall:
        ordered_comp_schemes.append(x[0])

    x_ax = [1, 2, 3, 4, 5, 6]
    bar_width = 0.2
    for comp, xp in zip(ordered_comp_schemes, x_ax):
        lupine_av = np.average(totals_dict["lupine"][comp])
        aws_av = np.average(totals_dict["aws"][comp])
        ubuntu_av = np.average(totals_dict["ubuntu"][comp])
        plt.bar(xp, lupine_av/1000.0, width=bar_width, edgecolor=lupine_color, hatch="\\\\\\", color="white")
        xp += bar_width
        plt.bar(xp, aws_av/1000.0, width=bar_width, edgecolor=aws_color, hatch="...", color="white")
        xp += bar_width
        plt.bar(xp, ubuntu_av/1000.0, width=bar_width, edgecolor=ubuntu_color, hatch="///", color="white")

    x_ticks = [x + bar_width for x in x_ax]
    plt.xticks(x_ticks, ordered_comp_schemes)
    plt.legend(handles=legend)
    plt.ylabel("Time (ms)")
    
    plt.savefig("./graphs/compression-bakeoff.pdf", format='pdf')
    plt.cla()

if __name__ == "__main__":
    compression_bakeoff()