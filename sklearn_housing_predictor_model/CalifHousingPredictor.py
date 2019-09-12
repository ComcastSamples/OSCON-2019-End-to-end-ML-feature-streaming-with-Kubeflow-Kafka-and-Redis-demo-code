import pickle
import sys

class CalifHousingPredictor(object):

    def __init__(self):
        # load the saved trained model
        model_file = 'example_model.pkl'
        self.sklearn_model = pickle.load(open(model_file, 'rb'))
        # required so you don't hit the 
        #  "TypeError: '<' not supported between instances of 'NoneType' and 'int'" bug
        self.sklearn_model.n_estimators = 100
        self.sklearn_model.n_jobs = 1

    def predict(self, X, features_names):
        return self.sklearn_model.predict(X)

