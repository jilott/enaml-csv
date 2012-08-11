from traits.api import HasTraits, String, Dict

class ScriptHandler(HasTraits):
    '''
    A class to execute the script in the text editor and manage the generated
    variables.
    '''
    
    # The script itself, fetched through the get_text() method of the
    # TextEditor
    script = String
    
    # Global variables
    my_locals = Dict
    
    # Local variables after 'exec'uting the script
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