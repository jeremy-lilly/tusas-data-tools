#!/usr/projects/hpcsoft/spack-paraview/cray-sles15-zen2/paraview/gcc-12.1.0/paraview-5.10.1-sh43pwemz5ljp34wpp7jklzxflbklqez/bin/pvpython


from paraview.simple import *

import argparse as ap


def main(file, out, time):
    # create a new 'IOSS Reader'
    results = IOSSReader(registrationName='results', FileName=[file])

    # get the time-keeper, move to final time
    timeKeeper = GetTimeKeeper()
    finalTime = timeKeeper.TimestepValues[time]
    UpdatePipeline(time=finalTime, proxy=results)

    # get active view
    renderView = GetActiveViewOrCreate('RenderView')

    # current camera placement for renderView
    renderView.InteractionMode = '2D'
    renderView.CameraPosition = [1911.2685622012252, 893.5010100912012, 7630.409257346341]
    renderView.CameraFocalPoint = [1911.2685622012252, 893.5010100912012, 0.0]
    renderView.CameraParallelScale = 923.1409390528261

    # get layout
    layout = GetLayout()
    layout.SetSize(1536, 730)

    # get animation scene
    animationScene = GetAnimationScene()
    animationScene.UpdateAnimationUsingDataTimeSteps()

    # Properties modified on renderView
    renderView.UseColorPaletteForBackground = 0
    renderView.Background = [1.0, 1.0, 1.0]
    renderView.OrientationAxesVisibility = 0

    # set active source
    SetActiveSource(results)

    # show data in view
    resultsDisplay = Show(results, renderView, 'UnstructuredGridRepresentation')
    resultsDisplay.Representation = 'Surface'
    ColorBy(resultsDisplay, ('POINTS', 'pp0'))
    resultsDisplay.RescaleTransferFunctionToDataRange(True, False)
    resultsDisplay.SetScalarBarVisibility(renderView, True)

    # get 2D transfer function for 'pp0'
    #pp0TF2D = GetTransferFunction2D('pp0')
    pp0LUT = GetColorTransferFunction('pp0')
    #pp0LUT.TransferFunction2D = pp0TF2D
    pp0LUT.RGBPoints = [3.3746602361278053, 0.231373, 0.298039, 0.752941, 
                        7.687304622007792, 0.865003, 0.865003, 0.865003, 
                        11.999949007887778, 0.705882, 0.0156863, 0.14902]
    pp0LUT.ScalarRangeInitialized = 1.0

    # get opacity transfer function/opacity map for 'pp0'
    pp0PWF = GetOpacityTransferFunction('pp0')
    pp0PWF.Points = [3.3746602361278053, 0.0, 0.5, 0.0, 
                     11.999949007887778, 1.0, 0.5, 0.0]
    pp0PWF.ScalarRangeInitialized = 1

    # Apply a preset using its name 
    pp0LUT.ApplyPreset('Jet', True)

    # get color legend/bar for pp0LUT in view renderView1
    pp0LUTColorBar = GetScalarBar(pp0LUT, renderView)
    pp0LUTColorBar.Title = 'pp0'
    pp0LUTColorBar.ComponentTitle = ''

    # Properties modified on pp0LUTColorBar
    pp0LUTColorBar.TitleColor = [0.0, 0.0, 0.0]
    pp0LUTColorBar.LabelColor = [0.0, 0.0, 0.0]

    # export view
    ExportView(out, view=renderView, Compressoutputfile=0)

    return 
# END main()


if __name__ == '__main__':
    parser = ap.ArgumentParser()

    parser.add_argument('-f', '--file', dest='file',
                        type=str,
                        required=False,
                        default='results.e',
                        help='Name of input results file.')

    parser.add_argument('-o', '--out', dest='out',
                        type=str,
                        required=False,
                        default='out.pdf',
                        help='Name for output visualization file.')

    parser.add_argument('-t', '--time', dest='time',
                        type=int,
                        required=False,
                        default=-1,
                        help='Time index to visualize.')

    args = parser.parse_args()

    main(args.file, args.out, args.time)
# END if
