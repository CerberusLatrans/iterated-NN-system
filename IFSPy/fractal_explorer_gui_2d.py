import sys
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt

from ifs import iterate, ifs_interpolate
from catalogue.leaves import FERN2D, MAPLE2D
from markov import weighted_random_chooser, MarkovIterator
from visualize import render_points, points_to_coordinates
import random
import numpy as np

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.label = QtWidgets.QLabel()
        self.dim = (200,200)
        canvas = QtGui.QPixmap(*self.dim)
        canvas.fill(Qt.white)
        self.label.setPixmap(canvas)
        self.setCentralWidget(self.label)

        self.ifs_chain = ifs_interpolate(FERN2D, MAPLE2D)
        
        button = QtWidgets.QPushButton("Press Me!")
        button.clicked.connect(self.render_ifs)
        self.setMenuWidget(button)

        self.parallelograms = []
        self.selected = None

    def add_parallelogram(self):
        self.parallelograms.append(Parallelogram())

    def remove_parallelogram(self):
        if self.selected is not None:
            self.parallelograms.remove(self.selected)

    def render_ifs(self):
        ifs = self.ifs_chain[random.choice(range(len(self.ifs_chain)))]
        self.display(MarkovIterator(ifs), 10_000)

    def display(self, iterator, n):      
        canvas = self.label.pixmap()
        canvas.fill()

        painter = QtGui.QPainter(canvas)
        for x,y in points_to_coordinates(iterate(iterator, n, multi=True), self.dim):
            painter.drawPoint(x,y)
        painter.end()

        self.label.setPixmap(canvas)

"""Once selected:
Translate: Drag middle point
Scale X: Drag Left or Right Side
Scale Y: Drag Top or Bottom Side
Rotate: Shift + scroll
Shear X: Shift + drag top or bottom horizontally
Shear Y: Shift + drag left or right vertically
"""

class Parallelogram():
    pass
app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()