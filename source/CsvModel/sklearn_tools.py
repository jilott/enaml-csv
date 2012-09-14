from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.linear_model import Perceptron, RidgeClassifier, SGDClassifier
from sklearn.naive_bayes import BernoulliNB, MultinomialNB
from sklearn.neighbors import KNeighborsClassifier, NearestCentroid
from scipy.sparse.csr import csr_matrix
from traits.api import HasTraits, Instance, Float, CInt, String, Dict
from pandas import DataFrame
from selection_handler import SelectionHandler
import pickle




class TextClassifier(HasTraits):
    
    # The text vectorizer from sklearn.feature_extraction.text
    vectorizer = Instance(TfidfVectorizer)
    
    # The training data
    x_train = Instance(csr_matrix)
    
    # The testing data
    x_test = Instance(csr_matrix)
    
    # The average performance score of the classifier
    classifier_score = Float
    
    # Length of the selected column that should be considered as training data
    train_length = CInt(0)
    
    # The column index that should be considered as containing the targets
    target_col_no = CInt(0)
    
    # The DataFrame instance containing the data
    data_frame = Instance(DataFrame)
    
    # The selection_handler object for the tableview
    selection_handler = Instance(SelectionHandler)
    
    # The string representation of the selected classifier
    classifier_select = String
    
    # A dictionary that maps classifier_string into sklearn classifier
    # instances
    classifier_dict = Dict

    
    def __init__(self, vectorizer=None, data_frame=None):

        if vectorizer is not None:
            self.vectorizer = vectorizer
        else:
            self.vectorizer = TfidfVectorizer()
        if data_frame is not None:
            self.data_frame = data_frame
        self.selection_handler = SelectionHandler()
        self.classifier_dict = {
            'LinearSVC':LinearSVC(),
            'Perceptron':Perceptron(),
            'RidgeClassifier':RidgeClassifier(),
            'SGDClassifier':SGDClassifier(),
            'BernoulliNB':BernoulliNB(),
            'MultinomialNB':MultinomialNB(),
            'KneighborsClassifier':KNeighborsClassifier(),
            'NearestCentroid':NearestCentroid()
        }
    
    def select_classifier(self):
        '''
        Sets the classifier as per the selection from the user.
        '''
        self.classifier = self.classifier_dict[self.classifier_select]
    
    def create_dataset(self):
        '''
        Splits the data frame into training data, testing data and targets.
        '''
        
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
        '''
        Vectorizes the text input.
        '''
        self.x_train = self.vectorizer.fit_transform(self.training_data)
        #self.x_test = self.vectorizer.transform(self.testing_data)
    
    def train_classifier(self):
        '''
        Trains the selected classifier.
        '''
        self.classifier.fit(self.x_train, self.train_targets)
    
    def test_classifier(self):
        '''
        Tests the selected classifier to generate the prediction score.
        '''
        self.x_test = self.vectorizer.transform(self.testing_data)
        self.prediction = self.classifier.predict(self.x_test)
        self.classifier_score = self.classifier.score(self.x_test,
                                                      self.test_targets)
    
    def save_classifier(self, pickle_filename):
        '''
        Saves the classifier and vectorizer objects as a pickle file.
        '''
        op = open(pickle_filename, 'w')
        pickle.dump(self.classifier, op)
        pickle.dump(self.vectorizer, op)
        op.close()
    
    def load_classifier(self, pickle_filename):
        '''
        Loads a classifier and a vectorizer from a pickle file.
        '''
        op = open(pickle_filename, 'r')
        self.classifier = pickle.load(op)
        self.vectorizer = pickle.load(op)
        op.close()
    
    def make_prediction(self):
        '''
        Makes prediction considering the selected column as test input.
        '''
        self.selection_handler.create_selection()
        pred_data_index = self.selection_handler.selected_indices[0][1]
        pred_column_name = self.data_frame.columns[pred_data_index]
        self.testing_data = self.data_frame[pred_column_name]
        self.x_test = self.vectorizer.transform(self.testing_data)
        self.prediction = self.classifier.predict(self.x_test)