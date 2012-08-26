from traits.api import HasTraits, Bool, Instance, Int, Array, List,Dict
from traitsui.api import View, Item
from chaco.api import (
    Plot, ArrayPlotData, OverlayPlotContainer, marker_trait, PlotGrid,
    Legend
)

from enable.api import ColorTrait
from selection_handler import SelectionHandler


class XYPlotHandler(HasTraits):
    container = OverlayPlotContainer
    plotdata = ArrayPlotData
    plot = Plot
    color = ColorTrait("blue")
    marker = marker_trait
    marker_size = Int(4)
    selection_handler = Instance(SelectionHandler)
    plot_type_disc = Bool
    plot_type_cont = Bool
    table = Array
    grid_underlays = List
    plot_list_view = Dict
    view = View(
        Item('color'),
        Item('marker'),
        Item('marker_size')
    )
    def __init__(self):
        self.selection_handler = SelectionHandler()
        self.container = OverlayPlotContainer()
        self.underlays = []
    
    
    
        
    #def _selection_handler_default(self):
    #    return SelectionHandler()
    
    def add_xyplot_selection(self,plot_name):
        if self.selection_handler.xyplot_check():
            self.plotdata = ArrayPlotData(
                x=self.table[:,self.selection_handler.selected_indices[0][1]],
                y=self.table[:,self.selection_handler.selected_indices[1][1]]
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
            
            self.plot = plot
            
            for underlay in self.plot.underlays:
                if isinstance(underlay, PlotGrid):
                    if underlay not in self.grid_underlays:
                        self.grid_underlays.append(underlay)
            
            self.plot_list_view[plot_name]=self.plot
            self.container.add(self.plot)

            self.container.request_redraw()
            
        self.selection_handler.flush()

    def grid_toggle(self, checked):
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