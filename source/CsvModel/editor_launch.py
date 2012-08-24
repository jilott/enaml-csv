from CsvModel import CsvModel
from plot_handlers import XYPlotHandler

model = CsvModel()
xyplot_handler = XYPlotHandler()


if __name__ == '__main__':
    import enaml
    with enaml.imports():
        from layout import Main
        view = Main(model=model,xyplot_handler=xyplot_handler)
        view.show()