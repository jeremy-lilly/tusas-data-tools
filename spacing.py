#! /usr/bin/env python

import argparse as ap
import glob
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from tools import *


def main(file_list, x_pos, threshold, outname):

    # parse input data to pass to tools
    datapath = '/'.join(file_list[0].split('/')[:-1]) + '/'
    filename = datapath + f'{x_pos:g}.csv'
    
    xmin, xmax, ymin, ymax = get_mesh_dims(file_list)
    
    data = extract_line_data(filename, file_list, x_pos, ymin, ymax, threshold)

    # plot extracted data
    x = data['DataFrame']['arc_length'].values
    pp0 = data['DataFrame']['pp0'].values
    
    fig, ax = plt.subplots(1, 1)
    
    ax.plot(x, threshold * np.ones(x.shape[0]), 'k--')
    ax.plot(x, pp0)
    
    ax.scatter(data['x_relmax'], data['pp0_relmax'])
    ax.scatter(data['x_relmin'], data['pp0_relmin'])
    
    ax.set_ylabel('pp0')
    ax.set_xlabel('arc length')
    
    #ax.set_xlim([500, 700])
    
    fig.tight_layout()
    fig.savefig(outname)
    
    print(f'distances between dendrites = {data['dists']}')
    print(f'dendrites are paired = {data['pairs']}')

# END main()


if __name__ == '__main__':

    parser = ap.ArgumentParser()

    parser.add_argument('-f', '--files', dest='files',
                        type=str,
                        required=True,
                        nargs='+',
                        help='Path to output data with a wildcard.' +
                             'Ex: /path/to/results.e.8.*')

    parser.add_argument('-x', '--x-position', dest='x_pos',
                        type=float,
                        required=True,
                        help='x-position of data to extract/plot.')

    parser.add_argument('-t', '--threshold', dest='threshold',
                        default=6,
                        type=float,
                        help='Threshold value for whether dendrites are treated as paired.')

    parser.add_argument('-o', '--out', dest='outname',
                        default='out.png',
                        type=str,
                        help='Name and file extension for output plot.')

    args = parser.parse_args()
    
    main(args.files,
         args.x_pos,
         args.threshold,
         args.outname)

# END if
