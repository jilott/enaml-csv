from traits.api import List, Int, on_trait_change

from enaml.components.base_selection_model import BaseSelectionModel

from enaml.guard import guard


class ColumnSelectionModel(BaseSelectionModel):
    """ A selection model that maps to a list of column indices.

    """
    #: The selected row indices.
    selected_columns = List(Int)

    #: Only select rows.
    selection_behavior = 'columns'

    @on_trait_change('selection_event')
    def _update_columns(self, event):
        selected_columns = []
        for topleft, botright in self.get_selection():
            selected_columns.extend(range(topleft.column, botright.column+1))
        selected_columns.sort()
        with guard(self, self._update_columns):
            self.selected_columns = selected_columns

    @on_trait_change('selected_columns,selected_columns_items')
    def _update_selection(self):
        if guard.guarded(self, self._update_columns):
            return
        item_model = self.parent.item_model
        selection = []
        # FIXME: try to merge contiguous rows into ranges.
        for i in self.selected_columns:
            topleft = item_model.create_index(i, 0, item_model)
            botright = item_model.create_index(i, 0, item_model)
            selection.append((topleft, botright))
        self.set_selection(selection, ('clear_select', 'column'))
