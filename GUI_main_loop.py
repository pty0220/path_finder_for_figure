import sys
import vtk
import main_loop

from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import uic
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot


class Form2(QtWidgets.QDialog):
    def __init__(self, number_of_trandcuer, length_transducer2target, range_angle, centerline_vector, Target, spherePoly, ROC, width,
         frist_cutskull, focus, raycasting_length, skull_properties, water_properties, random_properties, startTime, Target_name,
         number_of_beamlines, beamline_mesh_mean, focal_length, skull_file_name,transducer_plot,interactor, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = uic.loadUi("main_loop.ui", self)
        self.ui.show()
        self.number_of_trandcuer= number_of_trandcuer
        self.length_transducer2target =length_transducer2target
        self.range_angle =range_angle
        self.centerline_vector =centerline_vector
        self.Target = Target
        self.spherePoly = spherePoly
        self.ROC =ROC
        self.width = width
        self.frist_cutskull = frist_cutskull
        self.focus = focus
        self.raycasting_length= raycasting_length
        self.skull_properties= skull_properties
        self.water_properties = water_properties
        self.random_properties = random_properties
        self.startTime =startTime
        self.Target_name = Target_name
        self.number_of_beamlines = number_of_beamlines
        self.beamline_mesh_mean =beamline_mesh_mean
        self.focal_length= focal_length
        self.skull_file_name = skull_file_name
        self.iren = interactor
        self.transducer_plot =transducer_plot





    @pyqtSlot()
    def main_loop(self):
        main_loop.loop(self.number_of_trandcuer,self.length_transducer2target,self.range_angle,self.centerline_vector,
                       self.Target,self.spherePoly,self.ROC,self.width,self.frist_cutskull,self.focus,self.raycasting_length,self.skull_properties
                       ,self.water_properties,self.random_properties,self.startTime, self.Target_name,self.number_of_beamlines, self.beamline_mesh_mean
                       ,self.focal_length,self.skull_file_name,self.transducer_plot,self.iren)