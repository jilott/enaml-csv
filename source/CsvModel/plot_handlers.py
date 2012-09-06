import numpy as np
from traits.api import HasTraits, Bool, Instance, Int, Array, List,Dict, String
from traitsui.api import View, Item
from chaco.api import (
    Plot, ArrayPlotData, OverlayPlotContainer, marker_trait, PlotGrid,
    Legend, ColorBar
)
from chaco.tools.api import ZoomTool, PanTool
from chaco.tools.traits_tool import TraitsTool
from chaco.example_support import COLOR_PALETTE
from enable.api import ColorTrait
from selection_handler import SelectionHandler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from pandas import DataFrame
from statsmodels.api import OLS
from matplotlib.mlab import find


class XYPlotHandler(HasTraits):
    '''
    Class for handling XY plots
    '''
    
    # Whether the data is a pandas dataframe
    AS_PANDAS_DATAFRAME = Bool
    
    # The container for all current plots. Gets updated everytime a plot is
    # added.
    container = OverlayPlotContainer    
    
    # This can be removed.
    plotdata = ArrayPlotData
    
    # The current Plot object.
    plot = Plot
    
    # ColorTrait, mainly required for the TraitsUIItem view.
    color = ColorTrait("blue")
    
    # Marker trait for the view
    marker = marker_trait
    
    # Marker size trait
    marker_size = Int(4)
    
    # An instance of SelectionHandler for adding plots from the current
    # selection.
    selection_handler = Instance(SelectionHandler)
    
    # Bool traits for checking the type of the plot (discrete / continuous)
    plot_type_disc = Bool
    plot_type_cont = Bool
    
    # The data from which to draw the plots, same as the table attribute of
    # CsvModel
    table = Array
    
    # The pandas data frame if AS_PANDAS_DATAFRAME
    data_frame = Instance(DataFrame)
    
    # Contains the grid underlays of all the current plots
    grid_underlays = List
    
    # Used for viewing the list of the plots and the legend
    plot_list_view = Dict
    
    # TraitsUI view for plot properties, yet to find an enaml implementation
    view = View(
        Item('color'),
        Item('marker'),
        Item('marker_size')
    )
    
    # The plot that is being edited.
    current_plot = Instance(Plot)
    
    def __init__(self):
        self.selection_handler = SelectionHandler()
        self.container = OverlayPlotContainer()
        self.underlays = []
    
    
    def add_xyplot_selection(self,plot_name):
        '''
        Called when the 'add plot from selection button is clicked.'
        '''
        
        self.selection_handler.create_selection()
        if self.selection_handler.xyplot_check():
            
            if self.AS_PANDAS_DATAFRAME:
                x_column = self.data_frame.columns[
                    self.selection_handler.selected_indices[0][1]
                ]
                y_column = self.data_frame.columns[
                    self.selection_handler.selected_indices[1][1]
                ]
                x = np.array(self.data_frame[x_column])
                y = np.array(self.data_frame[y_column])
                self.plotdata = ArrayPlotData(x=x,y=y)
            
            else:
                
                first_column = self.selection_handler.selected_indices[0]
                second_column = self.selection_handler.selected_indices[1]
                self.plotdata = ArrayPlotData(
                    x=self.table[:,first_column[1]],
                    y=self.table[:,second_column[1]]
                )
            
            plot = Plot(self.plotdata)
            
            if self.plot_type_disc:
                plot_type = 'scatter'
            else:
                plot_type = 'line'
            plot.plot(
                ("x","y"),type = plot_type,
                color = self.color,
                marker = self.marker,
                marker_size = self.marker_size
            )
            
            plot.tools.append(PanTool(plot))
            plot.tools.append(ZoomTool(plot))
            plot.tools.append(TraitsTool(plot))
            
            self.plot = plot
            
            for underlay in self.plot.underlays:
                if isinstance(underlay, PlotGrid):
                    if underlay not in self.grid_underlays:
                        self.grid_underlays.append(underlay)
            
            if plot_name == '':
                self.plot_list_view[
                    'plot'+str(len(self.plot_list_view))]=self.plot
            else:
                self.plot_list_view[plot_name]=self.plot
            self.container.add(self.plot)

            self.container.request_redraw()
            
        self.selection_handler.flush()

    def grid_toggle(self, checked):
        '''
        Called when the 'Show Grid' checkbox ins toggled
        '''
        if not checked:
            for plot in self.container.components:
                for underlay in self.grid_underlays:
                    if underlay in plot.underlays:
                        plot.underlays.remove(underlay)
        else:
            for plot in self.container.components:
                for underlay in self.grid_underlays:
                    if underlay not in plot.underlays:
                        plot.underlays.append(underlay)
        self.container.request_redraw()
    
    def remove_selected_plots(self,selection):
        '''
        Called when the 'Remove Selected Plots' button is clicked
        '''
        remove_indices = []
        for model_index in selection:
            remove_indices.append(model_index[0].row)
        remove_plots = []
        for index in remove_indices:
            remove_plots.append(self.plot_list_view.keys()[index])
        
        removed_plots = []
        for plot in remove_plots:
            removed_plots.append(self.plot_list_view.pop(plot))
        for plot in self.container.components:
            self.container.remove(plot)
        for plot in self.plot_list_view.keys():
            self.container.add(self.plot_list_view[plot])
        self.container.request_redraw()
    
    def edit_selection(self, show_grid, plot_visible, plot_type_disc):
        '''
        Called to start editing the selected plot. Should accompany the 'Edit
        Plot' dialog.
        '''
        
        self.selection_handler.create_selection()
        index = self.selection_handler.selected_indices[0][0]
        plot_name = self.plot_list_view.keys()[index]
        
        plot = self.plot_list_view[plot_name]
        self.container.remove(plot)
        
        
        self.plot_type_disc = plot_type_disc
        
        if self.plot_type_disc:
            plot_type = 'scatter'
        else:
            plot_type = 'line'
        
        plot = Plot(plot.data)
        plot.plot(
            ("x","y"),color=self.color, type = plot_type,
            marker = self.marker, marker_size = self.marker_size
        )
        self.plot = plot
        self.plot.visible = plot_visible
        
        grid_underlays = []
        
        if not show_grid:
            for underlay in self.plot.underlays:
                if isinstance(underlay,PlotGrid):
                    grid_underlays.append(underlay)
            for underlay in grid_underlays:
                self.plot.underlays.remove(underlay)
                    
        
        self.container.add(self.plot)
        self.container.request_redraw()
        
        self.selection_handler.flush()


class ImagePlotHandler(HasTraits):
    
    # the overlay container for the plot
    container = Instance(OverlayPlotContainer)
    
    # the selection handler instance for the tableview
    selection_handler = Instance(SelectionHandler)
    
    # the input data.
    table = Array
    
    # The chaco colorbar object accompanying the plot.
    colorbar = ColorBar
    
    def __init__(self):
        self.container = OverlayPlotContainer()
        plot = ArrayPlotData(imagedata=self.table)
        self.selection_handler = SelectionHandler()
        
    
    def imageplot_check(self):
        '''
        Called to check whether the current selection is compatible with an
        image plot.
        '''
        if len(self.selection_handler.selected_indices)>1:
            shape_list = []
            for index_tuple in self.selection_handler.selected_handler:
                x = self.table[index_tuple[0]:index_tuple[2],
                               index_tuple[1]:index_tuple[3]]
                shape_list.append(x.shape)
            shape_ = shape_list[0]
            if shape_list.count(shape_)!=len(shape_list):
                return False
            return True
        else:
            return True
    
    def toggle_colorbar(self, checked):
        '''
        Function called to toggle the colorbar on the image plot.
        '''
        if not checked:
            for component in self.container.components:
                if isinstance(component, ColorBar):
                    self.colorbar = component
            self.container.components.remove(self.colorbar)
        else:
            self.container.add(self.colorbar)
        self.container.request_redraw()

    
    def draw_image_plot(self):
        '''
        Function called to draw the image plot.
        '''
        self.top_left = self.selection_handler.selected_indices[0][0:2]
        self.bot_right = self.selection_handler.selected_indices[0][2:4]
        data = self.table[self.top_left[0]:self.bot_right[0],
                          self.top_left[1]:self.bot_right[1]]
        plotdata = ArrayPlotData(imagedata=data)
        plot = Plot(plotdata)
        plot.img_plot('imagedata')
        plot.tools.append(PanTool(plot))
        plot.tools.append(ZoomTool(plot))
        plot.tools.append(TraitsTool(plot))
        self.container.add(plot)
        
        #colorbar = ColorBar(
        #    index_mapper=LinearMapper(range=plot.color_mapper.range),
        #    color_mapper = plot.color_mapper,
        #    orientation='v'
        #)
        #self.colorbar = ColorBar
        #self.container.add(colorbar)
        
        self.container.request_redraw()


class PCPlotHandler(HasTraits):
    
    # The container for the plot.
    container = OverlayPlotContainer()
    
    # the sklearn.decmoposition.PCA object
    pca = PCA
    
    # Whether or not to normalize the data, one of the parameters of the PCA
    # object
    whiten = Bool
    
    # The input data.
    table = Array
    
    # The selection_handler instance for the tableview
    selection_handler = Instance(SelectionHandler)
    
    def __init__(self):
        self.pca = PCA(n_components = 2)
        self.pca.whiten = True
        self.container = OverlayPlotContainer()
        self.selection_handler = SelectionHandler()
    
    def draw_pc_plot(self):
        '''
        Called to draw the PCA plot.
        '''
        self.selection_handler.create_selection()
        if len(self.selection_handler.selected_indices)==1:
            top_left = self.selection_handler.selected_indices[0][0:2]
            bot_right = self.selection_handler.selected_indices[0][2:4]
            data = self.table[top_left[0]:bot_right[0],
                              top_left[1]:bot_right[1]]
            pc_red = self.pca.fit_transform(data)
            plotdata = ArrayPlotData(
                x = pc_red[:,0],
                y = pc_red[:,1]
            )
            plot = Plot(plotdata)
            plot.plot(("x","y"),type='scatter')
            self.container.add(plot)
            self.container.request_redraw()


class RegressionPlotHandler(HasTraits):
    
    # The input data from the csv file
    data = Array
    
    # The input, or the selected column / row
    Y = Array
    
    # OLS fitted values of the current selection
    selection_olsfit = Array
    
    # the index used to plot the output
    index = Array
    
    # the container for the plots
    container = Instance(OverlayPlotContainer)
    
    # The selection handler object for the tableview
    selection_handler = Instance(SelectionHandler)
    
    def __init__(self):
        self.selection_handler = SelectionHandler()
        self.container = OverlayPlotContainer()
    
    def fit_selection(self):
        '''
        Function that computes the curve to fit.
        '''
        self.selection_handler.create_selection()
        if len(self.selection_handler.selected_indices)==1:
            tuple_list = self.selection_handler.selected_indices[0]
            if tuple_list[1]==tuple_list[3]:
                L = tuple_list[2]-tuple_list[0]
                self.index = np.arange(L+1)
                self.Y = self.data[:,tuple_list[1]]

                results = OLS(self.Y,self.index).fit()
                self.selection_olsfit = results.fittedvalues
        self.selection_handler.flush()
    
    def plot_fits(self):
        '''
        Function called to plot the regression fits.
        '''
        components = []
        
        for component in self.container.components:
            components.append(component)
        
        for component in components:
            self.container.components.remove(component)
                
        
        plotdata = ArrayPlotData(x=self.index, y=self.Y)
        plot = Plot(plotdata)
        plot.plot(("x","y"),type='line',color='red')
        plot.line_style = 'dash'
        self.container.add(plot)
        
        plotdata = ArrayPlotData(x=self.index,y=self.selection_olsfit)
        plot = Plot(plotdata)
        plot.plot(("x","y"),type='line',color='blue')
        self.container.add(plot)
        
        self.container.request_redraw()

class HistogramPlotHandler(HasTraits):
    
    # Index for the histogram plot
    index = Array
    
    # The selection handler object for the selected data
    selection_handler = Instance(SelectionHandler)
    
    # OVerlayPlotContainer for the histogram plot
    container = Instance(OverlayPlotContainer)
    
    # Number of bins of the histogram
    nbins = Int(10)
    
    # Whether the data is a pandas dataframe or a numpy array
    AS_PANDAS_DATAFRAME = Bool
    
    def __init__(self):
        self.index = range(self.nbins)
        self.selection_handler = SelectionHandler()
        self.container = OverlayPlotContainer()
    
    def draw_histogram(self):
        '''
        Default function called when drawing the histogram.
        '''
        for component in self.container.components:
            self.container.remove(component)
            
        self.selection_handler.create_selection()
        
        if len(self.selection_handler.selected_indices)==1:
            tuple_list = self.selection_handler.selected_indices[0]
            if self.AS_PANDAS_DATAFRAME:
                column_name = self.data.columns[tuple_list[1]]
                y = self.data[column_name]
                self.index = np.arange(self.nbins)
                hist = np.histogram(y, self.nbins)[0]
                plotdata = ArrayPlotData(x=self.index,y=hist)
                plot = Plot(plotdata)
                plot.plot(("x","y"),type='bar',bar_width=0.5)
                self.container.add(plot)
            else:
                column = tuple_list[1]
                y = self.data[:,column]
                self.index = np.arange(self.nbins)
                hist = np.histogram(y, self.nbins)[0]
                plotdata = ArrayPlotData(x=self.index,y=hist)
                plot = Plot(plotdata)
                plot.plot(("x","y"),type='bar',bar_width=0.5)
                self.container.add(plot)
            
            self.container.request_redraw()
    
        self.selection_handler.flush()

class KMeansPlotHandler(HasTraits):
    
    # the data to cluster
    data = Array
    
    # the dataset created after preprocessing
    dataset = Array
    
    # the sklearn.cluster.KMeans object
    kmeans = Instance(KMeans)
    
    # Number of clusters
    n_clusters = Int
    
    # Maximum iterations for the clustering algorithm
    max_iter = Int
    
    # Container for the cluster plots
    container = Instance(OverlayPlotContainer)
    
    # the columns from the dataset to omit when performing clustering
    to_omit = List
    
    
    def __init__(self):
        self.kmeans = KMeans()
        self.container = OverlayPlotContainer()
    
    def create_dataset(self):
        
        if self.to_omit:
            if len(self.to_omit)>0:
                n_rows = self.data.shape[0]
                n_cols = self.data.shape[1]
                to_omit = []
                for elem in self.to_omit:
                    if elem.isdigit():
                        to_omit.append(int(elem))
                
                dataset = self.data[:,0].reshape((n_rows,1))
                
                for elem in range(n_cols):
                    if elem not in to_omit:
                        if elem > 0:
                            dataset = np.hstack((dataset,
                                                 self.data[:,elem].reshape((
                                                    n_rows,1))))
            self.dataset = dataset
        
       
    

    def plot_clusters(self):
        
        self.kmeans.n_clusters = self.n_clusters
        self.kmeans.fit(self.dataset)
        
        # Reducing dimensions of the dataset and the cluster centers for
        # plottting
        pca = PCA(n_components=2, whiten=True)
        cluster_centers = pca.fit_transform(self.kmeans.cluster_centers_)
        dataset_red = pca.fit_transform(self.dataset)
        
        removed_components = []
        for component in self.container.components:
            removed_components.append(component)
        
        for component in removed_components:
            self.container.remove(component)
        
        for i in range(self.n_clusters):
            
            current_indices = find(self.kmeans.labels_==i)
            current_data = dataset_red[current_indices,:]
            
            plotdata = ArrayPlotData(x=current_data[:,0], y=current_data[:,1])
            plot = Plot(plotdata)
            plot.plot(("x","y"),type='scatter',color=tuple(COLOR_PALETTE[i]))
            self.container.add(plot)
            
            
        plotdata_cent = ArrayPlotData(x=cluster_centers[:,0],
                                      y=cluster_centers[:,1])
        plot_cent = Plot(plotdata_cent)
        plot_cent.plot(("x","y"),type='scatter',marker='cross',marker_size=8)
        self.container.add(plot_cent)
        
        self.container.request_redraw()

