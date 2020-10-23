#!/usr/bin/python3

import math
import sys
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib
import logging
logging.disable(sys.maxsize)

# TODO: paramatre olarak al -r rmsf, -a angle, -d dihedral, -t torsion 
# TODO: -c combined ile data tek grafikte seçeneği
# TODO: dafault rmsd, step size 0.05


def generate_plot_histogram(df_file, stepsize):
    for column in range(1, len(df_file.columns)):
        collection = {}
        sum = 0
        for i, row in df_file.iterrows():
            data = float(row[column])
            index = int(math.floor(data/stepsize))
            try:
                collection[index] += 1.
            except:
                collection[index] = 1.
            sum += 1

        indexes = list(collection.keys())
        #sorted(indexes)
        indexes.sort()
        minIndex = indexes[0]
        maxIndex = indexes[-1]
        d = []
        for i in range(minIndex, maxIndex+1):
            try:
                proba = collection[i]*1.0/sum
                n = collection[i]
            except:
                proba = 0.0
                n = 0
            d.append((i*stepsize, proba, n))

        ax = plt.gca()
        ax.legend(bbox_to_anchor=(1.1, 1.05))
        df_hist = pd.DataFrame(d, columns=('stepsize', df_file.columns[column], 'n'))
        df_hist.plot(kind='line', x='stepsize', y=df_file.columns[column], ax=ax, antialiased=True)
        plt.xlabel('RMSD (' + r'$\AA$)')
        plt.ylabel("Probability")
        ax.set_xlim([0, 3])
        #plt.legend(loc=9, bbox_to_anchor=(0.5, -0.1), ncol=3)
        plt.savefig(df_file.columns[column] + '-hist.png', bbox_inches='tight', dpi=300)
        plt.close()


def generate_plots(df):
    for c in list(df.columns[1:]):
        ax = plt.gca()
        ax.set_ylim([0, 3])
        df.plot(kind='line', x='#Frame', y=c, ax=ax, antialiased=True)

        #plt.xlabel('Frame')
        #plt.ylabel('Distance (' + r'$\AA$)')

        plt.xlabel('Frame')
        plt.ylabel('RMSD (' + r'$\AA$)')

        #plt.ylabel('RMSF')
        #plt.legend([c], loc=9, bbox_to_anchor=(0.5, -0.1), ncol=3)
        plt.savefig(c + '.png', bbox_inches="tight", dpi=300)
        plt.close()


if __name__ == "__main__":
    if len(sys.argv) >= 3:
        data_file = sys.argv[1]
        df = pd.DataFrame()
        df = pd.read_csv(data_file, delim_whitespace=True) 

        generate_plots(df)
        generate_plot_histogram(df, float(sys.argv[2]))
    else:
        print("usage: histogram.py <str:datafile> <float:hist_step_size>")

