from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from scipy.sparse.csr import csr_matrix
from traits.api import HasTraits, Instance, Float, CInt
from pandas import DataFrame
from selection_handler import SelectionHandler


class DataExtractor(HasTraits):
    pass




class TextClassifier(HasTraits):
    
    vectorizer = Instance(TfidfVectorizer)
    x_train = Instance(csr_matrix)
    x_test = Instance(csr_matrix)
    classifier_score = Float
    train_length = CInt(0)
    target_col_no = CInt(0)
    data_frame = Instance(DataFrame)
    selection_handler = Instance(SelectionHandler)
    

    
    def __init__(self, vectorizer=None, classifier=None, data_frame=None):

        if vectorizer is not None:
            self.vectorizer = vectorizer
        else:
            self.vectorizer = TfidfVectorizer()
        if classifier is not None:
            self.classifier = classifier
        else:
            self.classifier = LinearSVC()
        if data_frame is not None:
            self.data_frame = data_frame
        self.selection_handler = SelectionHandler()
    
    def create_dataset(self):
        
        self.selection_handler.create_selection()
        column = self.selection_handler.selected_indices[0][1]
        column_name = self.data_frame.columns[column]
        data = self.data_frame[column_name]
        self.training_data = data[:self.train_length]
        self.testing_data = data[self.train_length:]
        
        column_name = self.data_frame.columns[self.target_col_no]
        target_data = self.data_frame[column_name]
        self.train_targets = target_data[:self.train_length]
        self.test_targets = target_data[self.train_length:]
        
        self.selection_handler.flush()
    
    def text_vectorize(self):
        self.x_train = self.vectorizer.fit_transform(self.training_data)
        self.x_test = self.vectorizer.transform(self.testing_data)
    
    def train_classifier(self):
        self.classifier.fit(self.x_train, self.train_targets)
    
    def test_classifier(self):
        self.prediction = self.classifier.predict(self.x_test)
        self.classifier_score = self.classifier.score(self.x_test,
                                                      self.test_targets)
    