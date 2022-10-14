import os
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QTabWidget, QLineEdit, QComboBox, QPushButton
from math import pi

os.chdir(os.path.dirname(__file__))

class AA(QMainWindow):

    def __init__(self):
        """
        Initialise the application.
        """
        super(AA, self).__init__()

        # Load the ui file
        uic.loadUi("main.ui", self)

        # Define widgets
        self.defineWidgets()

        # Assign fonction
        self.asignWidgetsToFunction()

        #
        self.computed_once = False

        # Show the app
        self.show()

    def defineWidgets(self):
        """
        Defines all widget used in the application.
        """
        # Tabs
        self.tabs = self.findChild(QTabWidget, "tabs")

        # Density
        self.density_input = self.findChild(QLineEdit, "density_input")
        self.density_unit = self.findChild(QComboBox, "density_unit")

        # Mass flow
        self.mass_flow_input = self.findChild(QLineEdit, "mass_flow_input")
        self.mass_flow_unit = self.findChild(QComboBox, "mass_flow_unit")

        # Exterior diameter
        self.ext_diameter_input = self.findChild(QLineEdit, "ext_diameter_input")
        self.ext_diameter_unit = self.findChild(QComboBox, "ext_diameter_unit")

        # Thickness
        self.thickness_input = self.findChild(QLineEdit, "thickness_input")
        self.thickness_unit = self.findChild(QComboBox, "thickness_unit")

        # Result
        self.result_output = self.findChild(QLineEdit, "result_output")
        self.result_unit = self.findChild(QComboBox, "result_unit")

        # Compute
        self.compute_button = self.findChild(QPushButton, "compute")

        # Reset
        self.reset_button = self.findChild(QPushButton, "reset")

    
    def asignWidgetsToFunction(self):
        """
        Assign a function to each widget.
        """

        # Compute
        self.compute_button.clicked.connect(self.startComputing)

        # Reset
        self.reset_button.clicked.connect(self.resetComputeUI)

    
    def startComputing(self):
        """
        Start the computation.
        """
        if self.allInputsFilled():
            if not self.computed_once:
                self.computeSpeed()
            else:
                if self.density_input.isModified() or self.mass_flow_input.isModified() or self.ext_diameter_input.isModified() or self.thickness_input.isModified():
                    self.computeSpeed()


    def allInputsFilled(self):
        """
        Checks if all inputs fields are filled.

        Returns:
            bool: True if all inputs are filled.
        """
        if self.density_input.text() and self.mass_flow_input.text() and self.ext_diameter_input.text() and self.thickness_input.text():
            return True
        return False

    
    def allInputsCorrect(self, density, mass_flow, ext_diameter, thickness):
        """
        Check if all inputs are correct.

        Args:
            density (float): density of the fluid (kg/m3).
            mass_flow (float): mass flow (kg/h).
            ext_diameter (float): outer diameter of the pipe (m).
            thickness (float): thickness of the pipe (m).

        Returns:
            _type_: _description_
        """
        if density <= 0 or mass_flow <= 0 or ext_diameter <= 0 or thickness <= 0:
            return False
        return True



    def computeSpeed(self):
        """
        Compute the speed of the gas in the pipe.
        """

        # Parameters
        density = 0
        mass_flow = 0
        ext_diameter = 0
        thickness = 0

        # Speed in m/s
        if self.result_unit.currentText() == "m/s":
            # Density
            if self.density_unit.currentText() == "kg/m^3":
                try:
                    density = float(self.density_input.text())
                except:
                    self.density_input.clear()
            # Mass flow
            if self.mass_flow_unit.currentText() == "kg/h":
                try:
                    mass_flow = float(self.mass_flow_input.text())
                except:
                    self.mass_flow_input.clear()
            # Ext. diameter
            if self.ext_diameter_unit.currentText() == "m":
                try:
                    ext_diameter = float(self.ext_diameter_input.text())
                except:
                    self.ext_diameter_input.clear()
            elif self.ext_diameter_unit.currentText() == "cm":
                try:
                    ext_diameter = float(self.ext_diameter_input.text()) / 100
                except:
                    self.ext_diameter_input.clear()
            elif self.ext_diameter_unit.currentText() == "mm":
                try:
                    ext_diameter = float(self.ext_diameter_input.text()) / 1000
                except:
                    self.ext_diameter_input.clear()
            # Thickness
            if self.thickness_unit.currentText() == "m":
                try:
                    thickness = float(self.thickness_input.text())
                except:
                    self.thickness_input.clear()
            elif self.thickness_unit.currentText() == "cm":
                try:
                    thickness = float(self.thickness_input.text()) / 100
                except:
                    self.thickness_input.clear()
            elif self.thickness_unit.currentText() == "mm":
                try:
                    thickness = float(self.thickness_input.text()) / 1000
                except:
                    self.thickness_input.clear()

        if self.allInputsCorrect(density, mass_flow, ext_diameter, thickness):
            speed = self.computeFunction(density, mass_flow, ext_diameter, thickness)
            self.result_output.setText(str(speed))


    def computeFunction(self, density, mass_flow, ext_diameter, thickness):
        """
        Compute the speed in m/s of a fluid caracterised by its density, in a pipe with a given outer diameter and thickness, where the mass flow is known.

        Args:
            density (float): density of the fluid (kg/m3).
            mass_flow (float): mass flow (kg/h).
            ext_diameter (float): outer diameter of the pipe (m).
            thickness (float): thickness of the pipe (m).
        """

        volumetric_flow = (mass_flow / density) / 3600

        inner_radius = (ext_diameter / 2) - thickness
        inner_section = pi * inner_radius**2

        return volumetric_flow / inner_section


    def resetComputeUI(self):
        """
        Clear all inputs and outputs in the compute tab.
        """

        # Reset all inputs
        self.density_input.clear()
        self.mass_flow_input.clear()
        self.ext_diameter_input.clear()
        self.thickness_input.clear()

        # Reset output
        self.result_output.clear()


# Initialise the app
app = QApplication(sys.argv)
window = AA()
app.exec_()
