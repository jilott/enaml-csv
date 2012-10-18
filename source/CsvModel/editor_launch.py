from csv_model import CsvModel
from plot_handlers import (XYPlotHandler, ImagePlotHandler, PCPlotHandler,
RegressionPlotHandler, HistogramPlotHandler, KMeansPlotHandler)
from sklearn_tools import TextClassifier, MLEvaluator
from pandas.io.parsers import read_csv
import os
import pickle
import sys


model = CsvModel()
xyplot_handler = XYPlotHandler()
imageplot_handler=ImagePlotHandler()
pcplot_handler = PCPlotHandler()
regressplot = RegressionPlotHandler()
histplot_handler = HistogramPlotHandler()
kmeans_plot = KMeansPlotHandler()
text_class = TextClassifier()
ml_evaluator = MLEvaluator()



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
    
    this_path = os.path.abspath(__file__)
    model_dir = os.path.dirname(this_path)
    command_history_file = os.path.join(model_dir, 'command_history.pkl')
    
    if os.path.isfile(command_history_file):
        f = open(command_history_file, 'r')
        command_history = pickle.load(f)
        model.script_handler.command_history = command_history
        f.close()
    
    
    
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
            kmeans_plot = kmeans_plot,
            text_class = text_class,
            ml_evaluator = ml_evaluator
        )
        view.show()


this_path = os.path.abspath(__file__)
model_dir = os.path.dirname(this_path)
command_history_file = os.path.join(model_dir, 'command_history.pkl')

if os.path.isfile(command_history_file):
    f = open(command_history_file, 'r')
    command_history = pickle.load(f)
    model.script_handler.command_history = command_history
    f.close()

if len(sys.argv)>1:
    model.filename = sys.argv[1]
    model.data_frame = read_csv(model.filename)


    

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
                    kmeans_plot = kmeans_plot,
                    text_class = text_class,
                    ml_evaluator = ml_evaluator)
        view.show()