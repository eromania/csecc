#!/usr/bin/python

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

SMALL_SIZE = 10
MEDIUM_SIZE = 16
BIGGER_SIZE = 18

plt.rc('font', size=SMALL_SIZE)
plt.rc('axes', titlesize=SMALL_SIZE)
plt.rc('axes', labelsize=MEDIUM_SIZE)
plt.rc('xtick', labelsize=SMALL_SIZE)
plt.rc('ytick', labelsize=SMALL_SIZE)
plt.rc('legend', fontsize=MEDIUM_SIZE)
plt.rc('figure', titlesize=BIGGER_SIZE)


def heatmap(data, row_labels, col_labels, ax=None, cbar_kw={}, cbarlabel="", **kwargs):

    if not ax:
        ax = plt.gca()

    im = ax.imshow(data, **kwargs)

    ax.set_xticks(np.arange(data.shape[1]))
    ax.set_yticks(np.arange(data.shape[0]))
    ax.set_xticklabels(col_labels)
    ax.set_yticklabels(row_labels)

    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",rotation_mode="anchor")

    for edge, spine in ax.spines.items():
        spine.set_visible(False)

    ax.set_xticks(np.arange(data.shape[1]+1)-.5, minor=True)
    ax.set_yticks(np.arange(data.shape[0]+1)-.5, minor=True)
    ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
    ax.tick_params(which="minor", bottom=False, left=False)

    return im

def annotate_heatmap(im, data=None, valfmt="{x:.2f}", textcolors=["black", "white"], threshold=None, **textkw):

    if not isinstance(data, (list, np.ndarray)):
        data = im.get_array()

    if threshold is not None:
        threshold = im.norm(threshold)
    else:
        threshold = im.norm(data.max())/2.

    kw = dict(horizontalalignment="center", verticalalignment="center")
    kw.update(textkw)

    if isinstance(valfmt, str):
        valfmt = matplotlib.ticker.StrMethodFormatter(valfmt)

    texts = []
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            kw.update(color=textcolors[int(im.norm(data[i, j]) > threshold)])
            text = im.axes.text(j, i, valfmt(data[i, j], None),fontsize=7, **kw)
            texts.append(text)

    return texts

def plot(data,ax,title,tx):
    im  = heatmap(data, simulations, labels, ax=ax, cmap="Blues", vmin=0, vmax=130)
    texts = annotate_heatmap(im, valfmt="{x:.2f}")
    ax.set_xticklabels([])
    plt.gcf().text(tx, 0.97, title, fontsize=10)
    plt.subplots_adjust(left=0.3)
    plt.grid(b=None)
    return im

simulations = ["sim-00", "sim-01", "sim-02", "sim-03", "sim-04", "sim-05", "sim-06", "sim-07", "sim-08", "sim-09"]

#labels = ["First Frame", "Last Frame", "Min", "Max"]
labels = ["" ""]


rmsd_PS1_A = np.array(
    [
[     151.93,     105.03 ],
[     165.30,     133.20 ],
[     171.39,     143.29 ],
[     161.18,     125.36 ],
[     156.69,     125.79 ],
[     156.39,     126.54 ],
[     160.70,     142.18 ],
[     155.06,     105.03 ],
[     164.14,     131.51 ],
[     146.12,      91.94 ]
    ])

rmsd_PS1_B = np.array(
    [
[     151.50,      80.44 ],
[     161.40,     132.91 ],
[     152.96,     142.58 ],
[     159.05,     123.13 ],
[     155.99,     123.98 ],
[     163.97,      82.57 ],
[     156.82,     139.15 ],
[     167.70,     116.88 ],
[     156.89,     134.51 ],
[     153.43,     123.42 ]
    ])

rmsd_PS5_A = np.array(
    [
[     155.67,       0.00 ],
[     150.74,      26.43 ],
[     170.38,     162.50 ],
[     160.77,      14.82 ],
[     165.87,     121.40 ],
[     165.02,      33.24 ],
[     160.72,       0.00 ],
[     155.52,      36.41 ],
[     159.32,     132.60 ],
[     165.11,     155.67 ]
    ])

rmsd_PS5_B = np.array(
    [
[     165.31,      23.18 ],
[     169.85,      15.69 ],
[     164.48,     143.11 ],
[     163.76,     128.61 ],
[     156.09,      58.34 ],
[     156.31,       8.08 ],
[     165.98,       1.89 ],
[     161.25,      33.73 ],
[     167.95,     122.31 ],
[     150.41,      -0.00 ]
    ])


fig, ((ax, ax2, ax3, ax4)) = plt.subplots(nrows=1, ncols=4, sharex=True, sharey=True)

plot(rmsd_PS1_A,ax, 'Chain-A', 0.14)
plot(rmsd_PS1_B,ax2,'Chain-B', 0.30)
im = plot(rmsd_PS5_A,ax3, 'Chain-A', 0.46)
plot(rmsd_PS5_B,ax4,'Chain-B', 0.64)

fig.tight_layout()
fig.subplots_adjust(right=0.75)
cbar_ax = fig.add_axes([0.75, 0.20, 0.05, 0.7])
cbar = fig.colorbar(im, cax=cbar_ax )
cbar.set_label(r'Contact ($\AA^2$)')

plt.gcf().text(0.23, 0.00, 'PS-I', fontsize=MEDIUM_SIZE)
plt.gcf().text(0.56, 0.00, 'PS-V', fontsize=MEDIUM_SIZE)

fname="heatmap"
plt.savefig(fname+'.png', format='png', dpi=300)
