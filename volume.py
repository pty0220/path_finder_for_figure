import vtk
import numpy as np
import helpfunction as hlp
import isosurface as iso

from vtk.util import numpy_support as ns
from F_interactorstyle import FStyle


l2n = lambda l: np.array(l)
n2l = lambda n: list(n)
ren = vtk.vtkRenderer()
i = 0

def pressure_map(i,top_point):
    grid, c2p, bounds, maximum_pressure, pointnumber = iso.Data_arange('SMA_result_full_vtk'+str(i)+'.vtk')



    # reader = vtk.vtkRectilinearGridReader()
    # reader.SetFileName(vtk_filename)
    # reader.Update()
    # grid = reader.GetOutput()
    bounds = grid.GetBounds()
    dimension  = grid.GetDimensions()
    extent = grid.GetExtent()
    vtk_coordi = grid.GetXCoordinates()
    xcoordi = ns.vtk_to_numpy(vtk_coordi)
    space = 1000*(xcoordi[1]- xcoordi[0])
    bounds = l2n(bounds)*1000

    image = vtk.vtkImageData()
    image.DeepCopy(grid)
    image.SetDimensions(dimension)
    image.SetExtent(extent)
    image.SetSpacing(space,space,space)
    image.SetOrigin(bounds[0], bounds[2], bounds[4])
    #image.SetOrigin(bounds[0]+top_point[0],bounds[2]+top_point[1],bounds[4]+top_point[2])
    #image.SetOrigin(top_point[0],top_point[1],top_point[2])
    #image.SetOrigin(0,0,0)
    volumeMapper = vtk.vtkGPUVolumeRayCastMapper()
    volumeMapper.SetInputData(image)

    opacityTransfer = vtk.vtkPiecewiseFunction()
    opacityTransfer.AddPoint(0,0)
    opacityTransfer.AddPoint(0.15,0.9999)
    opacityTransfer.AddPoint(0.7,0.999999)
    #opacityTransfer.AddPoint(0.8,0.6)
    opacityTransfer.AddPoint(0.8,0.99999999)


    ctf = vtk.vtkColorTransferFunction()
    ctf.AddRGBPoint(0.15, 0.1,0.1,1.0)
    ctf.AddRGBPoint(0.5, 0.2,1.0,0.2)
    ctf.AddRGBPoint(0.9, 1.0,0.0,0.0)

    volumeProperty = vtk.vtkVolumeProperty()
    volumeProperty.SetColor(ctf)
    volumeProperty.SetScalarOpacity(opacityTransfer)
    volumeProperty.SetScalarOpacityUnitDistance(300)

    volume = vtk.vtkVolume()
    volume.SetMapper(volumeMapper)
    volume.SetProperty(volumeProperty)
    #volume.SetOrientation(100,100,100)
    #volume.RotateX(180)
    #test = volume.GetOrientation()



    # skull_opacity = 0.5
    # skull_cut_opacity = 1
    # pressure_map_opacity =0.6
    #
    # skull, skull_actor = hlp.read_skull_vtk('SMA_950_60_skull_transform'+str(i)+'.vtk',skull_opacity)
    #
    # cut_skull, cut_skull_actor  = hlp.cut_skull_loop(skull,[0,0,45.22],[0,0.2,-1],skull_cut_opacity)
    # target, target_actor = hlp.addPoint(ren,(0,0,55.22),[1,1,1],3)

    ####### make grid
    cubeAxesActor = vtk.vtkCubeAxesActor()
    cubeAxesActor.SetBounds(bounds)
    cubeAxesActor.SetCamera(ren.GetActiveCamera())
    cubeAxesActor.GetTitleTextProperty(0).SetColor(1.0,0.0,0.0)
    cubeAxesActor.GetLabelTextProperty(0).SetColor(1.0,0.0,0.0)

    cubeAxesActor.GetTitleTextProperty(1).SetColor(0.0,1.0,0.0)
    cubeAxesActor.GetLabelTextProperty(1).SetColor(0.0,1.0,0.0)

    cubeAxesActor.GetTitleTextProperty(2).SetColor(0.0,0.0,1.0)
    cubeAxesActor.GetLabelTextProperty(2).SetColor(0.0,0.0,1.0)

    cubeAxesActor.XAxisLabelVisibilityOff()
    cubeAxesActor.YAxisLabelVisibilityOff()
    cubeAxesActor.ZAxisLabelVisibilityOff()


    cubeAxesActor.DrawXGridlinesOn()
    cubeAxesActor.DrawYGridlinesOn()
    cubeAxesActor.DrawZGridlinesOn()

    #cubeAxesActor.SetGridLineLocation(vtk.VTK_GRID_LINES_FURTHEST)

    cubeAxesActor.SetGridLineLocation(cubeAxesActor.VTK_GRID_LINES_FURTHEST)
    cubeAxesActor.XAxisMinorTickVisibilityOff()
    cubeAxesActor.YAxisMinorTickVisibilityOff()
    cubeAxesActor.ZAxisMinorTickVisibilityOff()

    cubeAxesActor.GetXAxesLinesProperty().SetColor(1,1,1)
    cubeAxesActor.GetYAxesLinesProperty().SetColor(1, 1, 1)
    cubeAxesActor.GetZAxesLinesProperty().SetColor(1, 1, 1)

    cubeAxesActor.GetXAxesGridlinesProperty().SetColor(1,1,1)
    cubeAxesActor.GetYAxesGridlinesProperty().SetColor(1,1,1)
    cubeAxesActor.GetZAxesGridlinesProperty().SetColor(1,1,1)
    cubeAxesActor.RotateX(90)
    axes    = vtk.vtkAxesActor()
    axes.SetTotalLength(10, 10, 10)
    axes.AxisLabelsOff()

    return volume

#
# camera = vtk.vtkCamera()
# camera.SetPosition(-17.811284716425323, 659.4654808488033, 6.369545286961824)
# camera.SetFocalPoint(-40.21995368824083, 8.313481696227214, 91.98281035664556)
# camera.SetViewUp(0.8175244241836558, -0.12138218595061623, -0.5629566420223072)
#
# ren.SetActiveCamera(camera)
# ren.AddVolume(volume)
# ren.SetBackground(0,0,0)
# ren.AddActor(axes)
# ren.AddActor(cubeAxesActor)
# #ren.AddActor(cut_skull_actor)
# ren.AddActor(target_actor)
# ren.AddActor(transducer_actor)
# ren.AddActor(skull_actor)
# renWin = vtk.vtkRenderWindow()
# renWin.AddRenderer(ren)
# renWin.SetSize(500, 800)
#
# iren = vtk.vtkRenderWindowInteractor()
# iren.SetRenderWindow(renWin)
#
# # 14 100  256 500 800
#
# ######## scalar bar
# lut, pressure_map_mapper, pressure_map_actor = iso.pressure_plane_maker(grid, maximum_pressure, 0, 137, 68, 68, 0, 191,
#                                                                         pressure_map_opacity)
#
# scalarBar = vtk.vtkScalarBarActor()
# scalarBar.SetLookupTable(lut)
# scalarBar.GetTitleTextProperty().SetFontSize(100)
# scalarBar.GetTitleTextProperty().SetColor(1, 1, 1)
# scalarBar.GetLabelTextProperty().SetColor(1, 1, 1)
#
# scalarBar.SetTitle('Pressure ')
# scalarBar.SetMaximumHeightInPixels(250)
# scalarBar.SetMaximumWidthInPixels(100)
#
# scalar_bar_widget = vtk.vtkScalarBarWidget()
# scalar_bar_widget.SetInteractor(iren)
# scalar_bar_widget.SetScalarBarActor(scalarBar)
# scalar_bar_widget.On()
# #ren.AddActor(scalarBar)
#
# renWin.GetInteractor().SetInteractorStyle(FStyle(skull_actor,cut_skull_actor,iren))
# iren.Initialize()
# renWin.Render()
# #camera_position = camera.GetPosition()
# #print(camera_position)
# iren.Start()

