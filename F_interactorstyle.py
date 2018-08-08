import vtk

import sys
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import uic
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot



class FStyle(vtk.vtkInteractorStyleTrackballCamera):
    def __init__(self, actor1,actor2, interactor):

        self.iren = interactor
        self.actor1 = actor1
        self.actor2 = actor2
        self.bInRenderer = True
        self.AddObserver("MouseMoveEvent", self.onMove )
        self.AddObserver("RightButtonPressEvent", self.onRightButtonPress)
        self.AddObserver("KeyPressEvent", self.keypress)

    def keypress(self,obj,event):
        pass
        # key = self.iren.GetKeySym()
        # renderer = self.iren.GetRenderWindow().GetRenderers().GetFirstRenderer()
        #
        # if key =='1':
        #
        #     if self.bInRenderer:
        #         renderer.RemoveActor(self.actor1)
        #         self.bInRenderer = False
        #     else:
        #         renderer.AddActor(self.actor1)
        #         self.bInRenderer = True


    def onMove(self, obj, evnet):
        self.OnMouseMove()
        camera = self.GetInteractor().GetRenderWindow().GetRenderers().GetFirstRenderer().GetActiveCamera()

        print("#########################")
        print (camera.GetPosition())
        print(camera.GetFocalPoint())
        print(camera.GetViewUp())
        print("#########################")
    def onRightButtonPress(self, obj, event):
        pass


        # renderer = self.GetInteractor().GetRenderWindow().GetRenderers().GetFirstRenderer()
        #
        # if self.bInRenderer:
        #     renderer.RemoveActor(self.actor2)
        #     self.bInRenderer = False
        # else:
        #     renderer.AddActor(self.actor2)
        #     self.bInRenderer = True
        #
        # self.GetInteractor().GetRenderWindow().Render()
        #
