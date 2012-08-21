# Classes for converting ModelIndices into

from traits.api import HasTraits, List


class SelectionHandler(HasTraits):
    
    current_selection = List
    selected_indices = List
    
    def _current_selection_default(self):
        return []
    
    def _selected_indices_default(self):
        return []
    
    def create_selection(self):
        for elem in self.current_selection:
            self.selected_indices.append(
                (elem[0].row,
                 elem[0].column,
                 elem[1].row,
                 elem[1].column)
            )
    
    def flush(self):
        self.curren_selection = []
        self.selected_indices = []