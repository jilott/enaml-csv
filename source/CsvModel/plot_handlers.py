from traits.api import HasTraits, Bool, Instance, Int, Array
from traitsui.api import View, Item
from chaco.api import Plot, ArrayPlotData, OverlayPlotContainer, marker_trait
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
    view = View(
        Item('color'),
        Item('marker'),
        Item('marker_size')
    )
    def __init__(self):
        self.selection_handler = SelectionHandler()
        self.container = OverlayPlotContainer()
    
    
    
    #def _selection_handler_default(self):
    #    return SelectionHandler()
    
    def add_xyplot_selection(self):
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
            self.container.add(self.plot)
            
            self.container.request_redraw()
            
        self.selection_handler.flush()