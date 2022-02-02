import matplotlib
from matplotlib import pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.patches import Patch
import numpy as np
import os
from matplotlib.pyplot import bar, figure
import re

if os.path.isdir("./results/lebench/"):
    RESULTS_PATH = "./results/lebench/"
else:
    RESULTS_PATH = "./results-paper/lebench/"

colors=mcolors.CSS4_COLORS
fgkaslr_color=colors["darkcyan"]
kaslr_color=colors["mediumseagreen"]

def lebench():

    baseline_path = RESULTS_PATH + "output.nokaslr.csv"
    baseline_f = open(baseline_path)
    baseline_flines = baseline_f.readlines()

    baseline_flines_kernel = baseline_flines[1].split(',')[1]
    print(baseline_flines_kernel)
    baseline_data_all = baseline_flines[2:]
    baseline_data_av = []
    for line in baseline_data_all:
        if "average" in line:
            baseline_data_av.append(line)
    baseline_test_names = []
    baseline_test_averages = []

    for line in baseline_data_av:
        line = line.replace("average", "")
        line = line.replace(" ", "")
        line = line.replace(":", "")
        line = line.replace("\n", "")
        line = re.split(',', line)
        baseline_test_names.append(line[0])
        baseline_test_averages.append(float(line[1]))

    kaslr_path = RESULTS_PATH +  "output.kaslr.csv"
    kaslr_f = open(kaslr_path)
    kaslr_flines = kaslr_f.readlines()

    kaslr_flines_kernel = kaslr_flines[1].split(',')[1]
    kaslr_data_all = kaslr_flines[2:]
    kaslr_data_av = []
    for line in kaslr_data_all:
        if "average" in line:
            kaslr_data_av.append(line)

    kaslr_test_averages = []
    for line in kaslr_data_av:
        line = line.replace("average", "")
        line = line.replace(" ", "")
        line = line.replace(":", "")
        line = line.replace("\n", "")
        line = re.split(',', line)
        kaslr_test_averages.append(float(line[1]))


    fgkaslr_path = RESULTS_PATH +  "output.fgkaslr.csv"
    fgkaslr_f = open(fgkaslr_path)
    fgkaslr_flines = fgkaslr_f.readlines()

    fgkaslr_flines_kernel = fgkaslr_flines[1].split(',')[1]
    fgkaslr_data_all = fgkaslr_flines[2:]
    fgkaslr_data_av = []
    for line in fgkaslr_data_all:
        if "average" in line:
            fgkaslr_data_av.append(line)

    fgkaslr_test_averages = []
    for line in fgkaslr_data_av:
        line = line.replace("average", "")
        line = line.replace(" ", "")
        line = line.replace(":", "")
        line = line.replace("\n", "")
        line = re.split(',', line)
        fgkaslr_test_averages.append(float(line[1]))


    kaslr_normal = [x/y for x, y in zip(kaslr_test_averages, baseline_test_averages)]
    fgkaslr_normal = [x/y for x, y in zip(fgkaslr_test_averages, baseline_test_averages)]
    x = [i*1.5 for i in range(len(kaslr_normal))]

    figure(figsize=(11,2.75))
    ax = plt.gca()
    ax.set_ylim([0, 2])
    ax.set_xlim([-0.75, x[len(x)-1] + 1])

    legend=[
        Patch(facecolor=kaslr_color, label="In-Monitor KASLR"),
        Patch(facecolor=fgkaslr_color
    , label="In-Monitor FG_KASLR")
    ]

    plt.hlines(1, -0.75, x[len(x)-1] + 1, linestyles='dotted', colors="black")

    for i in range(len(kaslr_normal)):
        plt.bar(
            x[i], 
            kaslr_normal[i],
            width=0.4,
            color=kaslr_color
        )
        plt.bar(
            x[i] + 0.4, 
            fgkaslr_normal[i],
            width=0.4,
            color=fgkaslr_color
        
        )

  

    plt.xticks(x, baseline_test_names, rotation=-30, ha='left')
    plt.legend(handles=legend)
    plt.ylabel("Relative Runtime")
    plt.tight_layout()
   
    plt.savefig("./graphs/lebench.pdf", format='pdf')

if __name__ == '__main__':
    lebench()