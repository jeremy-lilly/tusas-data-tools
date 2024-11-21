#!/Applications/ParaView-5.11.2.app/Contents/bin/pvpython

from paraview.simple import *

import argparse as ap


def main(files, out, start, end):

    # read in data
    data = IOSSReader(registrationName='results',
                      FileName=files)

    # get the time-keeper, move to final time
    timeKeeper = GetTimeKeeper()
    finalTime = timeKeeper.TimestepValues[-1]
    UpdatePipeline(time=finalTime, proxy=data)

    # only pass the data we need to PlotOverLine
    passArrays = PassArrays(registrationName='PassArrays',
                            Input=data)
    passArrays.PointDataArrays = ['pp0']
    passArrays.CellDataArrays = []

    # get data over line
    plotOverLine = PlotOverLine(registrationName='PlotOverLine',
                                Input=passArrays)
    plotOverLine.Point1 = start
    plotOverLine.Point2 = end

    # save data
    SaveData(out, proxy=plotOverLine,
             PointDataArrays=['arc_length', 'pp0', 'vtkValidPointMask'])

# END main()


if __name__  == '__main__':

    parser = ap.ArgumentParser()

    parser.add_argument('-f', '--files', dest='files',
                        nargs='+',
                        required=True,
                        help='Files to open.')

    parser.add_argument('-o', '--out', dest='out',
                        default='out.csv',
                        help='Name of output file in .csv format.')

    parser.add_argument('-s', '--line-start', dest='line_start',
                        type=float,
                        nargs=3,
                        required=True,
                        help='(x, y, z) for the start point of the line.')

    parser.add_argument('-e', '--line-end', dest='line_end',
                        type=float,
                        nargs=3,
                        required=True,
                        help='(x, y, z) for the end point of the line.')

    args = parser.parse_args()

    main(args.files,
         args.out,
         args.line_start,
         args.line_end)

# END if

