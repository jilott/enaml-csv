#!/usr/bin/env python

import numpy as np
import csv
from traits.api import File, HasTraits, Array, List, Instance
from enaml.stdlib.table_model import TableModel
from chaco.api import Plot, ArrayPlotData
from sklearn.decomposition import PCA

class CsvModel(HasTraits):
    
    filename = File
    table = Array
    headers = List
    pca = Instance(PCA,())
    xvsy_indices = (0,1)
    table_model = Instance(TableModel,())
    img_plotdata = Instance(ArrayPlotData,())
    image_plot = Instance(Plot,())
    xvsy_plotdata = Instance(ArrayPlotData, ())
    x_vs_y_plot = Instance(Plot, ())
    pca_plotdata = Instance(ArrayPlotData,())
    pca_plot = Instance(Plot,())
    
    def __init__(self):
        self.pca = PCA(n_components=2)
        self.pca.whiten = True
    
    def _table_default(self):
        x = np.zeros((100,100))
        return x
    
    def _table_model_default(self):
        tblmodel = TableModel(self.table, editable=True)
        return tblmodel
    
    def _image_plot_default(self):
        self.img_plotdata = ArrayPlotData(imagedata=self.table)
        p = Plot(self.img_plotdata)
        p.img_plot('imagedata')
        return p
    
    def _x_vs_y_plot_default(self):
        self.xvsy_plotdata = ArrayPlotData(x=self.table[:,self.xvsy_indices[0]],
                                           y=self.table[:,self.xvsy_indices[1]])
        p = Plot(self.xvsy_plotdata)
        p.plot(("x","y"), type='scatter',color='auto')
        return p
    
    def _pca_plot_default(self):
        pc_red = self.pca.fit_transform(self.table[0:100,:])
        self.pca_plotdata = ArrayPlotData(x=pc_red[:,0],y=pc_red[:,1])
        pca_plot = Plot(self.pca_plotdata)
        pca_plot.plot(("x","y"),type='scatter',color='auto')
        return pca_plot
    
    def _filename_changed(self, new):
        self.table = np.genfromtxt(self.filename, delimiter=',', skip_header=1)
        csv_reader= csv.reader(file(self.filename))
        self.headers = csv_reader.next()
        del csv_reader
        self.table_model = TableModel(self.table, editable=True,
                                 horizontal_headers=self.headers)
        self.img_plotdata.set_data('imagedata',self.table)
    
    