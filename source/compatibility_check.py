#!/usr/bin/env python

from traits.api import HasTraits, Bool, Instance

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
        pass
    
    def check_image_compatible(self):
        pass
    
    def check_pc_compatible(self):
        pass
    
    def check_histogram_compatible(self):
        pass
    
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