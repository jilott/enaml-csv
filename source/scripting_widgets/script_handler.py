from traits.api import HasTraits, String, Dict

class ScriptHandler(HasTraits):
    script = String
    my_locals = Dict
    my_globals = Dict
    
    def _script_default(self):
        return ''
    
    def _my_locals_default(self):
        return {}
    
    def _my_globals_default(self):
        return {}
    
    def exec_script(self):
        exec(self.script) in self.my_globals, self.my_locals
    
    def _my_locals_items_changed(self, new):
        # Implement this to change items in the workspace view
        pass