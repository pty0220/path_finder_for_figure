import sys
import vtk
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import uic
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot

import helpfunction as hlp




class Form(QtWidgets.QDialog):


    def __init__(self,skull_actor,skull_cut_actor,brain_actor,focus_actor,transducer_actor,a_range_actor,centerline_actor,firstline_actor,secondline_actor,finalline_actor, out_vector_actor,in_vector_actor,interactor,a_point_actor, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = uic.loadUi("switch.ui", self)
        self.ui.show()
        self.iren = interactor
        self.skull_actor = skull_actor
        self.skull_cut_actor = skull_cut_actor
        self.brain_actor= brain_actor
        self.focus_actor = focus_actor
        self.transducer_actor =transducer_actor
        self.a_range_actor = a_range_actor
        self.centerline_actor = centerline_actor
        self.firstline_actor= firstline_actor
        self.secondline_actor = secondline_actor
        self.finalline_actor= finalline_actor
        self.out_vector_actor = out_vector_actor
        self.in_vector_actor = in_vector_actor
        self.a_point_actor =a_point_actor


        self.skull = True
        self.skull_cut = True
        self.brain = True
        self.target = True
        self.transducer = True
        self.a_range = True
        self.centerline = True
        self.all =True
        self.first_beam_lines = True
        self.second_beam_lines = True
        self.final_beam_lines = True
        self.out_vector =True
        self.in_vector = True

    def Redraw(self):
        self.iren.GetRenderWindow().Render()

    @pyqtSlot()
    def All(self):
        renderer = self.iren.GetRenderWindow().GetRenderers().GetFirstRenderer()

        if self.all:
            renderer.AddActor(self.skull_actor)
            renderer.AddActor(self.skull_cut_actor)
            renderer.AddActor(self.brain_actor)
            renderer.AddActor(self.focus_actor)
            renderer.AddActor(self.transducer_actor)
            renderer.AddActor(self.a_range_actor)
            renderer.AddActor(self.centerline_actor)
            renderer.AddActor(self.out_vector_actor)
            renderer.AddActor(self.in_vector_actor)
            for i in range(len(self.firstline_actor)):
                renderer.AddActor(self.firstline_actor[str(i)])
            for i in range(len(self.secondline_actor)):
                renderer.AddActor(list(self.secondline_actor.values())[i])
            for i in range(len(self.finalline_actor)):
                renderer.AddActor(list(self.finalline_actor.values())[i])


            print("All on")
            self.all = False
            self.skull = False
            self.skull_cut = False
            self.brain = False
            self.target = False
            self.transducer = False
            self.a_range = False
            self.centerline = False
            self.all = False
            self.first_beam_lines = False
            self.second_beam_lines = False
            self.final_beam_lines = False
            self.out_vector = False
            self.in_vector = False

        else:
            renderer.RemoveActor(self.skull_actor)
            renderer.RemoveActor(self.skull_cut_actor)
            renderer.RemoveActor(self.brain_actor)
            renderer.RemoveActor(self.focus_actor)
            renderer.RemoveActor(self.transducer_actor)
            renderer.RemoveActor(self.a_range_actor)
            renderer.RemoveActor(self.centerline_actor)
            renderer.RemoveActor(self.out_vector_actor)
            renderer.RemoveActor(self.in_vector_actor)
            for i in range(len(self.firstline_actor)):
                renderer.RemoveActor(self.firstline_actor[str(i)])
            for i in range(len(self.secondline_actor)):
                renderer.RemoveActor(list(self.secondline_actor.values())[i])
            for i in range(len(self.finalline_actor)):
                renderer.RemoveActor(list(self.finalline_actor.values())[i])

            print("All off")
            self.skull = True
            self.skull_cut = True
            self.brain = True
            self.target = True
            self.transducer = True
            self.a_range = True
            self.centerline = True
            self.all = True
            self.first_beam_lines =True
            self.second_beam_lines = True
            self.final_beam_lines = True
            self.out_vector = True
            self.in_vector = True
        self.Redraw()


    @pyqtSlot()
    def Skull(self):
        renderer = self.iren.GetRenderWindow().GetRenderers().GetFirstRenderer()

        if self.skull:
            renderer.AddActor(self.skull_actor)
            print("Skull on")
            self.skull = False
        else:
            renderer.RemoveActor(self.skull_actor)
            print("Skull off")
            self.skull = True

        self.Redraw()


    @pyqtSlot()
    def Skull_Part(self):
        renderer = self.iren.GetRenderWindow().GetRenderers().GetFirstRenderer()

        if self.skull_cut:

            renderer.AddActor(self.skull_cut_actor)
            print("Skull_Part on")
            self.skull_cut = False
        else:
            renderer.RemoveActor(self.skull_cut_actor)

            print("Skull_Part off")
            self.skull_cut = True

        self.Redraw()



    @pyqtSlot()
    def Brain(self):
        renderer = self.iren.GetRenderWindow().GetRenderers().GetFirstRenderer()

        if self.brain:
            renderer.AddActor(self.brain_actor)
            print("Brain on")
            self.brain = False
        else:
            renderer.RemoveActor(self.brain_actor)


            print("Brain off")
            self.brain = True

        self.Redraw()



    @pyqtSlot()
    def Target(self):
        renderer = self.iren.GetRenderWindow().GetRenderers().GetFirstRenderer()

        if self.target:
            renderer.AddActor(self.focus_actor)
            print("Target on")
            self.target = False
        else:
            renderer.RemoveActor(self.focus_actor)
            print("Target off")
            self.target = True

        self.Redraw()



    @pyqtSlot()
    def Transducer(self):
        renderer = self.iren.GetRenderWindow().GetRenderers().GetFirstRenderer()

        if self.transducer:
            renderer.AddActor(self.transducer_actor)
            print("Transducer on")
            self.transducer = False
        else:
            renderer.RemoveActor(self.transducer_actor)
            print("Transducer off")
            self.transducer = True

        self.Redraw()




    @pyqtSlot()
    def Analysis_range(self):
        renderer = self.iren.GetRenderWindow().GetRenderers().GetFirstRenderer()
        if self.a_range:
            renderer.AddActor(self.a_range_actor)
            for i in range(len(self.a_point_actor)):
                renderer.AddActor(self.a_point_actor[str(i)])



            print("a_range on ")
            self.a_range = False
        else:
            renderer.RemoveActor(self.a_range_actor)
            for i in range(len(self.a_point_actor)):
                renderer.RemoveActor(self.a_point_actor[str(i)])



            print("a_range off")
            self.a_range = True

        self.Redraw()



    @pyqtSlot()
    def Center_line(self):
        renderer = self.iren.GetRenderWindow().GetRenderers().GetFirstRenderer()

        if self.centerline:
            renderer.AddActor(self.centerline_actor)
            print("centerline on")
            self.centerline = False
        else:
            renderer.RemoveActor(self.centerline_actor)
            print("centerline off")
            self.centerline = True

        self.Redraw()




    @pyqtSlot()
    def First_beam(self):
        renderer = self.iren.GetRenderWindow().GetRenderers().GetFirstRenderer()

        if self.first_beam_lines:

            for i in range(len(self.firstline_actor)):
                renderer.AddActor(self.firstline_actor[str(i)])


            print("beam_lines on")

            self.first_beam_lines = False


        else:


            for i in range(len(self.firstline_actor)):
                renderer.RemoveActor(self.firstline_actor[str(i)])

            print("beam_lines off")

            self.first_beam_lines = True

        self.Redraw()





    @pyqtSlot()
    def Second_beam(self):
        renderer = self.iren.GetRenderWindow().GetRenderers().GetFirstRenderer()

        if self.second_beam_lines:

            for i in range(len(self.secondline_actor)):
                renderer.AddActor(list(self.secondline_actor.values())[i])

            print("beam_lines on")
            self.second_beam_lines = False


        else:

            for i in range(len(self.secondline_actor)):
                renderer.RemoveActor(list(self.secondline_actor.values())[i])

            print("beam_lines off")
            self.second_beam_lines = True

        self.Redraw()





    @pyqtSlot()
    def Final_beam(self):
        renderer = self.iren.GetRenderWindow().GetRenderers().GetFirstRenderer()

        if self.final_beam_lines:

            for i in range(len(self.finalline_actor)):
                renderer.AddActor(list(self.finalline_actor.values())[i])

            print("beam_lines on")
            self.final_beam_lines = False

        else:

            for i in range(len(self.finalline_actor)):
                renderer.RemoveActor(list(self.finalline_actor.values())[i])
            print("beam_lines off")
            self.final_beam_lines = True

        self.Redraw()




    @pyqtSlot()
    def out_vector(self):
        renderer = self.iren.GetRenderWindow().GetRenderers().GetFirstRenderer()

        if self.out_vector:
            renderer.AddActor(self.out_vector_actor)
            print("out_vector on")
            self.out_vector = False


        else:
            renderer.RemoveActor(self.out_vector_actor)
            print("out_vector off")
            self.out_vector = True

        self.Redraw()


    @pyqtSlot()
    def in_vector(self):
        renderer = self.iren.GetRenderWindow().GetRenderers().GetFirstRenderer()

        if self.in_vector:
            renderer.AddActor(self.in_vector_actor)
            print("in_vector on")
            self.in_vector = False


        else:
            renderer.RemoveActor(self.in_vector_actor)
            print("out_vector off")
            self.in_vector = True

        self.Redraw()


    @pyqtSlot()
    def in_vector(self):
        renderer = self.iren.GetRenderWindow().GetRenderers().GetFirstRenderer()

        if self.in_vector:

            renderer.AddActor(self.in_vector_actor)
            print("in_vector on")
            self.in_vector = False


        else:
            renderer.RemoveActor(self.in_vector_actor)
            print("out_vector off")
            self.in_vector = True

        self.Redraw()


