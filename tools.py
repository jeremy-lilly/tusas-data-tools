import netCDF4 as nc
import numpy as np
import pandas as pd
from scipy.signal import argrelextrema
import subprocess as sp


def get_mesh_dims(file_list):
    top_data = nc.Dataset(file_list[0])
    bot_data = nc.Dataset(file_list[-1])

    xmax = np.max(top_data.variables['coordx'])
    xmin = np.min(bot_data.variables['coordx'])

    ymax = np.max(top_data.variables['coordy'])
    ymin = np.min(top_data.variables['coordy'])

    top_data.close()
    bot_data.close()

    return xmin, xmax, ymin, ymax 
# END get_mesh_dims()


def extract_line_data(filename, file_list, x_pos, ymin, ymax, threshold):
    try:
        df = pd.read_csv(filename, sep=',')
    except FileNotFoundError:
        print(f'{filename} not found, generating with ParaView...')

        files = ' '.join(file_list)
        sh_command = (f'./paraview_data_over_line.py ' + 
                      f'-f {files} ' +
                      f'-o {filename} ' +
                      f'-s {x_pos} {ymin} 0 ' + 
                      f'-e {x_pos} {ymax} 0')
        sp.run(sh_command.split())

        print('done.')

        df = pd.read_csv(filename, sep=',')
    # END try

    pp0 = df['pp0'].values
    x = df['arc_length'].values

    relmax_ind = argrelextrema(pp0, np.greater)
    x_relmax = x[relmax_ind]
    pp0_relmax = pp0[relmax_ind]

    relmin_ind = argrelextrema(pp0, np.less)
    x_relmin = x[relmin_ind]
    pp0_relmin = pp0[relmin_ind]

    # dists will hold the distances between peaks
    # i.e. index 0 will contain the distance
    # between peak 0 and peak 1
    dists = np.zeros(pp0_relmax.size - 1)

    # pairs will be a list of bools whether
    # subsequent peaks are 'pairs' in that
    # the relative minimum between them
    # is not below the threshold value
    # i.e. index 0 will contain the bool
    # for whether peak 0 and peak 1 are pairs
    pairs = np.zeros(pp0_relmax.size - 1)

    for i in range(pp0_relmax.size - 1):
        dists[i] = x_relmax[i + 1] - x_relmax[i]
        pairs[i] = pp0_relmin[i] > threshold
    # END for

    data = {}
    data['DataFrame'] = df
    data['relmin_ind'] = relmin_ind
    data['relmax_ind'] = relmax_ind
    data['x_relmin'] = x_relmin
    data['x_relmax'] = x_relmax
    data['pp0_relmin'] = pp0_relmin
    data['pp0_relmax'] = pp0_relmax
    data['dists'] = dists
    data['pairs'] = pairs

    return data

# END extract_line_data()

