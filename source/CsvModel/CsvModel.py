#!/usr/bin/env python

import numpy as np
import csv
from traits.api import (
    File, HasTraits, Array, List, Instance, Function, Int, Float, Bool
)
from enaml.stdlib.table_model import TableModel
from chaco.api import Plot, ArrayPlotData, marker_trait, OverlayPlotContainer
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from selection_handler import SelectionHandler
from enable.api import ColorTrait
from traitsui.api import View, Item

class PlotProperties(HasTraits):
    color = ColorTrait("blue")
    marker = marker_trait
    marker_size = Int(4)
    view = View(
        Item('color'),
        Item('marker'),
        Item('marker_size')
    )
    selection_handler = Instance(SelectionHandler)
    def add_xyplot_container(self):
        pass




class CsvModel(HasTraits):
    '''
    The object that is passed to the MainWindow of the enaml view. This
    represents a general model for different plots in the csv editor.
    '''
    
    # The .csv file to be opened.
    filename = File
    
    # The numpy array associated with the data in the file
    table = Array
    
    # The headers of the csv data
    headers = List
    
    # An sklearn.decomposition.PCA object, required for the
    # reduced-dimensionality plots
    pca = Instance(PCA)
    
    # Default indices for the X vs Y plot.
    xvsy_indices = (0,1)
    
    # Default row to be plotted in the histogram
    hist_row_index = Int(2)
    
    # Defulat number of bins for the histogram
    hist_nbins = Int(10)
    
    # The mean of the 2-D block of the array, represented by the current
    # selection
    block_mean = Float
    
    # The variance of the 2-D block of the array, represented by the current
    # selection
    block_var = Float
    
    # The standard deviation of the 2-D block of the array, represented by the
    # current selection
    block_std = Float
    
    # The TableModel instance to be passed to the item_model attribute of the
    # TableView
    table_model = Instance(TableModel,())
    
    # chaco.api.ArrayPlotData instance for the image plot
    img_plotdata = Instance(ArrayPlotData,())
    
    # chaco.api.plot instance for the image plot
    image_plot = Instance(Plot,())
    
    # chaco.api.ArrayPlotData instance for the XY plot
    xvsy_plotdata = Instance(ArrayPlotData, ())
    
    # chaco.api.plot instance for the image plot
    x_vs_y_plot = Instance(Plot, ())
    
    # Container for different XY plots
    xyplot_container = OverlayPlotContainer
    
    # chaco.api.ArrayPlotData instance for the PCA plot
    pca_plotdata = Instance(ArrayPlotData,())
    
    # chaco.api.plot instance for the pca plot
    pca_plot = Instance(Plot,())
    
    # chaco.api.ArrayPlotData instance for the histogram
    hist_plotdata = Instance(ArrayPlotData,())
    
    # chaco.api.plot instance for the histogram
    hist_plot = Instance(Plot,())
    
    # Class for handling selections from the TableView
    selection_handler = Instance(SelectionHandler)
    
    plot_type_disc = Bool
    
    plot_type_cont = Bool
    
    plot_properties = Instance(PlotProperties,())
    
    def __init__(self):
        '''
        So far only the PCA objects and the XY plot container needs to be 'initialized'.
        '''
        
        self.pca = PCA(n_components=2)
        self.pca.whiten = True
        self.xyplot_container = OverlayPlotContainer()
        self.plot_properties = PlotProperties()
    
    def _table_default(self):
        '''
        The default array in the TableView is a 100x100 array of zeros
        '''
        
        x = np.zeros((100,100))
        return x
    
    def _table_model_default(self):
        '''
        The default TableModel instance corresponding to the array of zeros
        '''
        
        tblmodel = TableModel(self.table, editable=True)
        return tblmodel
    
    def _image_plot_default(self):
        '''
        Default chaco plot object for the image plot.
        '''
        
        self.img_plotdata = ArrayPlotData(imagedata=self.table)
        p = Plot(self.img_plotdata)
        p.img_plot('imagedata')
        return p
    
    def _x_vs_y_plot_default(self):
        '''
        Default chaco plot object for the XY plot.
        '''
                
        self.xvsy_plotdata = ArrayPlotData(x=self.table[:,self.xvsy_indices[0]],
                                           y=self.table[:,self.xvsy_indices[1]])
        p = Plot(self.xvsy_plotdata)
        p.plot(("x","y"), type='scatter',color='auto')
        return p
    
    def _plot_type_disc_default(self):
        return True
    
    #def _pca_plot_default(self):
    #    '''
    #    Default chaco plot object for the PCA plot.
    #    '''
    #    
    #    #pc_red = self.pca.fit_transform(self.table[0:100,:])
    #    #self.pca_plotdata = ArrayPlotData(x=pc_red[:,0],y=pc_red[:,1])
    #    #pca_plot = Plot(self.pca_plotdata)
    #    #pca_plot.plot(("x","y"),type='scatter',color='auto')
    #    #return pca_plot
    #    return None
    
    def _hist_plot_default(self):
        '''
        Default chaco plot object for the histogram.
        '''
        
        h = np.histogram(self.table,10)[0]
        self.hist_plotdata = ArrayPlotData(x=h)
        p = Plot(self.hist_plotdata)
        p.plot('x',type='bar',color='auto',bar_width=0.3)
        return p
    
    def _selection_handler_default(self):
        return SelectionHandler()
    
    

    def _filename_changed(self, new):
        '''
        Executes whenever a file is loaded into the view.
        '''
        
        self.table = np.genfromtxt(self.filename, delimiter=',', skip_header=1)
        csv_reader= csv.reader(file(self.filename))
        self.headers = csv_reader.next()
        del csv_reader
        self.table_model = TableModel(self.table, editable=True,
                                 horizontal_headers=self.headers)
        self.img_plotdata.set_data('imagedata',self.table)
        self.xvsy_plotdata.set_data('x',self.table[:,self.xvsy_indices[0]])
        self.xvsy_plotdata.set_data('y',self.table[:,self.xvsy_indices[1]])
        self.hist_plotdata.set_data(
            'x',np.histogram(self.table[:,self.hist_row_index],self.hist_nbins)[0]
            )
    
    
    def use_selection_xyplot(self):
        indices = self.selection_handler.selected_indices
        if len(indices)>2:
            print 'X Y Plot not possible'
        else:
            if indices[0][0]!=indices[1][0] or indices[0][2]!=indices[1][2]:
                print 'X Y Plot not possible'
            else:
                self.xvsy_indices = (indices[0][1],
                                     indices[1][1])
        self.xvsy_plotdata.set_data('x',self.table[:,self.xvsy_indices[0]])
        self.xvsy_plotdata.set_data('y',self.table[:,self.xvsy_indices[1]])
    
    def create_plot_properties():
        pass
    
    # Used for adding an XY plot to the current container
    def add_xyplot_container(self):
        self.selection_handler.create_selection()
        if self.selection_handler.xyplot_check():
            plotdata = ArrayPlotData(
                x=self.table[:,self.selection_handler.selected_indices[0][1]],
                y=self.table[:,self.selection_handler.selected_indices[1][1]]
            )
            plot = Plot(plotdata)
            if self.plot_type_disc:
                plot_type = 'scatter'
            else:
                plot_type = 'line'
            plot.plot(
                ("x","y"),type = plot_type,
                color = self.plot_properties.color,
                marker = self.plot_properties.marker,
                marker_size = self.plot_properties.marker_size
            )
            self.xyplot_container.add(plot)
            self.xyplot_container.request_redraw()
        self.selection_handler.flush()
    
    def use_selection_preview(self):
        pass
    
    
    def use_selection_histogram(self):
        pass
    
    def use_selection_imageplot(self):
        pass
    
    def use_selection_pcaplot(self):
        pass