import os
from traits.api import HasTraits, Instance, String
from pandas.io.parsers import read_csv
from pandas import DataFrame

read_filename = os.path.join('..','..','..','ACM_bestbuy','train.csv')
write_filename = os.path.join('..','..','..','ACM_bestbuy','save_test.csv')

class SaveTest(HasTraits):
    
    read_filename = String
    write_filename = String
    
    data_frame = Instance(DataFrame)
    
    def __init__(self):
        self.read_filename = read_filename
        self.write_filename = write_filename
    
    def create_dataframe(self):
        self.data_frame = read_csv(read_filename)
    
    def save_dataframe(self):
        self.data_frame.to_csv(write_filename, index=False)

st = SaveTest()
st.create_dataframe()
st.save_dataframe()