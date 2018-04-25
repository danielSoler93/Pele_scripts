#/usr/bin/python2.7

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.widgets  import RectangleSelector
import numpy as np
import os
import errno
import argparse
import pandas as pd
import glob
import re
import sys
import interactivePlot as ip

"""

   Description: Plot a histogram of how many values in each range of values

   For any problem do not hesitate to contact us through the email address written below.

"""


__author__ = "Daniel Soler Viladrich"
__email__ = "daniel.soler@nostrumbiodiscovery.com"

OUTPUT_FOLDER = 'Counts'

def main(criteria, bin, output=OUTPUT_FOLDER, numfolders=False):

    reports = ip.find_reports(os.getcwd(),  numfolders)

    crit_name = get_column_names(reports, criteria)

    values = parse_values(reports, criteria,  crit_name)

    create_data = plot_histogram(values, bin, crit_name)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("crit", type=int, help="Number of column report we want to create the plot with. i.e 6")
    parser.add_argument("bin", type=int, help="Bin/Interval of the histogram. i.e 1")   
    parser.add_argument("--out", "-o", type=str, help="Output Path. i.e: BindingEnergies_apo", default=OUTPUT_FOLDER)
    parser.add_argument("--numfolders", "-nm", action="store_true", help="Not to parse non numerical folders")

    args = parser.parse_args()

    return args.crit, args.bin, args.out, args.numfolders

def parse_values(reports, criteria,  crit_name):
    """

       Description: Parse the 'reports' and create a sorted array
       of size n_structs following the criteria chosen by the user.

    """
    INITIAL_DATA = [
                  (crit_name, [])
                  ]
    min_values = pd.DataFrame.from_items(INITIAL_DATA)
    #min_values = pd.DataFrame(INITIAL_DATA)
    for file in reports:
        data = pd.read_csv(file, sep='    ', engine='python')
        selected_data = data.iloc[:, [criteria-1]]
        min_values = pd.concat([min_values, selected_data])
    return min_values 


def plot_histogram(values, bin, criteria):
    values_list = values[criteria].tolist()
    plt.hist(values_list, bin, rwidth=0.98)
    plt.title('Histogram')
    plt.xlabel(criteria)
    plt.ylabel('Counts')
    plt.show()


def get_column_names(reports, criteria):
    data = pd.read_csv(reports[0], sep='    ', engine='python')
    data = list(data)
    return data[criteria-1]

if __name__ == '__main__':
    crit, bin, out, num = parse_args()
    main(crit, bin, out, num)