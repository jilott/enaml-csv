from traits.api import List, HasTraits

class SelectionHandler(HasTraits):
    
    selection = List
    current_selection = List
    
    def _selection_default(self):
        return []
    
    def _current_selection_default(self):
        return []