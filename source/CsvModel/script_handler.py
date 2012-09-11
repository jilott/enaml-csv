from traits.api import HasTraits, String, Dict, List
import pickle
import os

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
    
    # The list of commands executed to date
    command_history = List
    
    def _script_default(self):
        return ''
    
    def _my_locals_default(self):
        return {}
    
    def _my_globals_default(self):
        return {}
    
    def exec_script(self):
        '''
        'Exec'utes the script in the text editor widget, the generated variables
        are in the local workspace, i.e. self.my_locals
        '''
        exec(self.script) in self.my_globals, self.my_locals
    
    def _my_locals_items_changed(self, new):
        # Implement this to change items in the workspace view
        pass
    
    def _command_history_default(self):
        return []
    
    def exec_single_line(self, clicked_event):
        command_index = clicked_event.new.row
        exec(self.command_history[command_index]) in self.my_globals, \
            self.my_locals
        self.command_history.append(self.command_history[command_index])
    
    def save_workspace(self):
        
        this_path = os.path.abspath(__file__)
        model_dir = os.path.dirname(this_path)
        command_history_file = os.path.join(model_dir, 'command_history.pkl')
        

        f = open(command_history_file, 'w')
        
        pickle.dump(self.command_history, f)
        f.close()
    
    def clear_history(self):
        
        this_path = os.path.abspath(__file__)
        model_dir = os.path.dirname(this_path)
        command_history_file = os.path.join(model_dir, 'command_history.pkl')
        
        if os.path.isfile(command_history_file):
            os.remove(command_history_file)
        
        self.command_history = []