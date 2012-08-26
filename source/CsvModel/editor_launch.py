from CsvModel import CsvModel
from plot_handlers import XYPlotHandler, ImagePlotHandler

model = CsvModel()
xyplot_handler = XYPlotHandler()
imageplot_handler=ImagePlotHandler()


if __name__ == '__main__':
    import enaml
    with enaml.imports():
        from layout import Main
        view = Main(model=model,xyplot_handler=xyplot_handler,
                    imageplot_handler=imageplot_handler)
        view.show()