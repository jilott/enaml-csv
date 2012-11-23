#!/usr/bin/env python

from traits.api import HasTraits, Bool, Instance, List
import numpy as np

class CompatibilityChecker(HasTraits):
    
    '''
    Class that checks whether the current selection is compatible with the
    data analysis and visualization widgets.
    '''
    
    # The current selection.
    selection = List
    
    # Whether the selection is compatible with an XY plot.
    xy_compatible = Bool
    
    # Whether the selection is compatible with an image plot.
    image_compatible = Bool
    
    # Whether the selection is compatible with a PCA decomposition and plotting.
    pc_compatible = Bool
    
    # Whether the selection is compatible with a histogram plot.
    histogram_compatible = Bool
    
    # Whether the selection is compatible witht a regression fit.
    regress_compatible = Bool
    
    # Whether the selection is compatible with displaying basic statistical
    # measurements.
    stats_compatible = Bool
    
    # Whether the selection is compatible with basic spreadsheet operations.
    spreadsheet_ops_compatible = Bool
    
    # Whether the selection is compatible with being introduced in a script as a
    # set of variables.
    scripting_compatible = Bool
    
    # Whether the selection is compatible with tokenization of the text within it.
    text_tokenize_compatible = Bool
    
    def check_xy_compatible(self):
        '''
        Returns true if the selection is compatible with an XY plot.
        '''
        if len(self.selection)!=2:
            self.xy_compatible = False
        else:
            a = np.array([self.selection[0][0].row, self.selection[0][0].column,
                          self.selection[0][1].row, self.selection[0][1].column])
            b = np.array([self.selection[1][0].row, self.selection[1][0].column,
                          self.selection[1][1].row, self.selection[1][1].column])
            d = a - b
            print d
            if (d[0]==d[2])|(d[1]==d[3]):
                self.xy_compatible = True
            else:
                self.xy_compatible = False
        
    
    def check_image_compatible(self):
        if len(self.selection)!=1:
            self.image_compatible = False
        else:
            top_left, bot_right = self.selection[0]
            if (top_left.row == bot_right.row)|(top_left.column==bot_right.column):
                self.image_compatible = False
            else:
                self.image_compatible = True
    
    def check_pc_compatible(self):
        
        self.check_xy_compatible()
        if self.xy_compatible:
            self.pc_compatible = False
            return
        
        self.check_image_compatible()
        if self.image_compatible:
            self.pc_compatible = True
            return
        
        if len(self.selection)>2:
            indices = np.zeros((len(self.selection),4),dtype=int)
            for i in range(indices.shape[0]):
                sel_tuple = self.selection[i]
                indices[i,:] = [
                    sel_tuple[0].row, sel_tuple[0].column, sel_tuple[1].row, sel_tuple[1].column
                ]
            
            v = indices.var(0)
            v = list(np.ceil(v).astype(int))
            if v.count(0)==2:
                self.pc_compatible = True
            else:
                self.pc_compatible = True

    def check_histogram_compatible(self):
        if len(self.selection)==1:
            top_left, bot_right = self.selection[0]
            if (top_left.row==bot_right.row)&(top_left.column==bot_right.column):
                self.histogram_compatible = False
            else:
                self.histogram_compatible = True
        else:
            self.histogram_compatible = True

    
    def check_regress_compatible(self):
        pass
    
    def check_stats_compatible(self):
        pass
    
    def check_spreadsheet_compatible(self):
        pass
    
    def check_scripting_compatible(self):
        pass
    
    def check_tokenize_compatible(self):
        pass
    
    