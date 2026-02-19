from network_security.constant.training_pipeline import SAVED_MODEL_DIR, MODEL_FILENAME
import os, sys
from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging

class NetworkModel:

    def __init__(self, preprocessor, model):
        try:
            self.preprocessor = preprocessor
            self.model = model
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def predict(self, X):
        try:
            X_transformed = self.preprocessor.transform(X)
            y_hat = model.predict(X_transformed)
            return y_hat
        except Exception as e:
            raise NetworkSecurityException(e, sys)