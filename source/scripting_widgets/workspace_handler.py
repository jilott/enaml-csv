import numpy as np
from enaml.core.item_model import AbstractItemModel, ALIGN_LEFT
from traits.api import Dict

class WorkspaceHandler(AbstractItemModel):
    
    workspace = Dict
    
    def __init__(self, workspace):
        self.workspace = workspace
        
    
    def index(self, row, column, parent=None):
        if self.has_index(row,column,parent=None):
            return self.create_index(row,column,None)
    
    def parent(self, index):
        pass
    
    def row_count(self, idx):
        if self.workspace.keys():
            return len(self.workspace.keys())
    
    def column_count(self, idx):
        return 4
    
    def horizontal_header_data(self, section):
        return ['Name', 'Type', 'Dimensions', 'Size (bytes)'][section]
    
    def data(self, idx):
        row = idx.row
        column = idx.column
        if column == 0:
            return self.workspace.keys()[row]
        elif column == 1:
            key = self.workspace.keys()[row]
            s = str(type(self.workspace[key]))
            return s.split('\'')[1]
        elif column == 2:
            key = self.workspace.keys()[row]
            if type(self.workspace[key]) is np.ndarray:
                return str(self.workspace[key].shape)                
            else:
                return 'N/A'
        else:
            key = self.workspace.keys()[row]
            return self.workspace[key].__sizeof__()
    
    def alignment(self, index):
        if index.column == 0:
            return ALIGN_LEFT
        return super(WorkspaceHandler, self).alignment(index)