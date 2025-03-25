#! /usr/bin/env python

import argparse as ap
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from tools import *


def main(file_list, x_pos, x_division, time, threshold, outname):
    xmin, xmax, ymin, ymax = get_mesh_dims(file_list)

    if x_division:
        x_pos = x_division * (xmax - xmin)
    # END if

    # parse input data to pass to tools
    datapath = '/'.join(file_list[0].split('/')[:-1]) + '/'
    filename = datapath + f'{x_pos:g}_{time}.csv'
    
    data = extract_line_data(filename, file_list,
                             x_pos, ymin, ymax,
                             threshold, time)
     
    # the total number of dendrites is equal to the number
    # relative maximums, minus the number of relative maximums
    # that don't have a relative min between them that is below
    # the given threshold
    num_dendrites = data['pp0_relmax'].shape[0]
    num_dendrites -= np.where(data['pairs'] == 1)[0].shape[0]
    
    # write info out to log
    log_file = '.'.join(filename.split('.')[:-1]) + f'_{threshold}.txt'
    log_msg = (f"distances between rel maximums = {data['dists']}\n" + 
               f"rel maximums are paired = {data['pairs']}\n" + 
               f"number of dendrites = {num_dendrites}\n" + 
               f"cross-section length = {ymax - ymin}\n" + 
               f"average dendrite spacing = {(ymax - ymin) / num_dendrites}\n")

    with open(log_file, 'w') as log:
        log.write(log_msg)
    # END with

    if outname:
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
        
        fig.tight_layout()
        fig.savefig(outname)
    # END if
# END main()


if __name__ == '__main__':

    parser = ap.ArgumentParser()

    parser.add_argument('-f', '--files', dest='files',
                        type=str,
                        required=True,
                        nargs='+',
                        help='Path to output data with a wildcard.' +
                             'Ex: /path/to/results.e.8.*')

    pos_group = parser.add_mutually_exclusive_group(required=True)
    pos_group.add_argument('-x', '--x-position', dest='x_pos',
                           type=float,
                           help='x-position of data to extract/plot.')
    pos_group.add_argument('-d', '--x-division', dest='x_division',
                           type=float,
                           help='Float giving the fractional position in the x-direction ' +
                                'to extract data.')

    parser.add_argument('-t','--time', dest='time',
                        type=int,
                        default=-1,
                        help='Time index.')

    parser.add_argument('-s', '--threshold', dest='threshold',
                        default=6,
                        type=float,
                        help='Threshold value for whether dendrites are treated as paired.')

    parser.add_argument('-o', '--out', dest='outname',
                        type=str,
                        help='Name and file extension for output plot.')

    args = parser.parse_args()
    
    main(args.files,
         args.x_pos,
         args.x_division,
         args.time,
         args.threshold,
         args.outname)

# END if

