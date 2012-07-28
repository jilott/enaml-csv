#!/usr/bin/env python

from chaco.api import Plot, ArrayPlotData
from traits.api import HasTraits, List, Array
from pandas import *
import numpy as np
import csv

csv_reader = csv.reader(file('sample.csv'))
nrows = 0
for row in csv_reader:
    nrows += 1
nrows = nrows - 1
ncols = len(row)

del csv_reader

csv_reader = csv.reader(file('sample.csv'))
headers = csv_reader.next()
x = np.genfromtxt('sample.csv', delimiter = ',', skip_header = 1)

#class MainWindow(HasTraits):
#    table = Array
#    headers = List
#    plot = Plot

class MyPlot:
    def __init__(self):
        x = np.ones((100,100))
        plotdata = ArrayPlotData(imagedata = x)
        plot = Plot(plotdata)
        plot.img_plot("imagedata")
        self.plot = plot

class MainWindow(HasTraits):
    table = Array
    headers = List
    plot = Plot

if __name__ == '__main__':
    import enaml
    with enaml.imports():
        from csv_editor_view import Main
        view = Main(mainwindow = MainWindow(table=x,
                                            headers=headers,
                                            plot = MyPlot().plot))
        view.show()


