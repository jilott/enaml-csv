from enaml.stdlib.table_model import TableModel

class DataFrameModel(TableModel):
    
    def data(self, index):
        row = self._data_source.index[index.row]
        column = self._data_source.columns[index.column]
        return self._display_data_converter(self._data_source[column][row])
