#!/usr/bin/env python

import numpy as np
import csv
from traits.api import File, HasTraits, Array, List, Instance
from enaml.stdlib.table_model import TableModel

class CsvModel(HasTraits):
    
    filename = File
    table = Array
    headers = List
    table_model = Instance(TableModel,())
    
    def _table_default(self):
        x = np.zeros((100,100))
        return x
    
    def _table_model_default(self):
        tblmodel = TableModel(self.table, editable=True)
        return tblmodel
    
    def _filename_changed(self, new):
        self.table = np.genfromtxt(self.filename, delimiter=',', skip_header=1)
        csv_reader= csv.reader(file(self.filename))
        self.headers = csv_reader.next()
        del csv_reader
        self.table_model = TableModel(self.table, editable=True,
                                 horizontal_headers=self.headers)