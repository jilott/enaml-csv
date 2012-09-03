from CsvModel import CsvModel
from plot_handlers import (XYPlotHandler, ImagePlotHandler, PCPlotHandler,
RegressionPlotHandler, HistogramPlotHandler, KMeansPlotHandler)

model = CsvModel()
xyplot_handler = XYPlotHandler()
imageplot_handler=ImagePlotHandler()
pcplot_handler = PCPlotHandler()
regressplot = RegressionPlotHandler()
histplot_handler = HistogramPlotHandler()
kmeans_plot = KMeansPlotHandler()




def enaml_editor_launch(x, AS_PANDAS=False):
    '''
    Called from terminal to launch the UI, for the data x
    '''
    model = CsvModel(data=x, AS_PANDAS_DATAFRAME=AS_PANDAS)
    xyplot_handler = XYPlotHandler()
    imageplot_handler=ImagePlotHandler()
    pcplot_handler = PCPlotHandler()
    regressplot = RegressionPlotHandler()
    histplot_handler = HistogramPlotHandler()
    kmeans_plot = KMeansPlotHandler()
    
    import enaml
    with enaml.imports():
        from layout import Main
        view =  Main(
            model = model,
            xyplot_handler=xyplot_handler,
            imageplot_handler=imageplot_handler,
            pcaplot_handler=pcplot_handler,
            regressplot = regressplot,
            histplot_handler=histplot_handler,
            kmeans_plot = kmeans_plot
        )
        view.show()

if __name__ == '__main__':
    import enaml
    with enaml.imports():
        from layout import Main
        view = Main(model=model,
                    xyplot_handler=xyplot_handler,
                    imageplot_handler=imageplot_handler,
                    pcaplot_handler=pcplot_handler,
                    regressplot = regressplot,
                    histplot_handler=histplot_handler,
                    kmeans_plot = kmeans_plot)
        view.show()