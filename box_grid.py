import numpy as np
import vtk


l2n = lambda l: np.array(l)
n2l = lambda n: list(n)

def cubeaxes(bounds):
    ren = vtk.vtkRenderer()
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

    return cubeAxesActor