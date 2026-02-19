import os, sys
from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import f1_score, precision_score, recall_score
import numpy as np

def evaluate_models(X_train:np.array, y_train:np.array, X_test:np.array, y_test:np.array, models:dict, params:dict)->dict:
    try:
        report = {}
        for name, model in models.items():
            param = params[name]
            gs = GridSearchCV(model, param_grid=param, cv=3, n_jobs=-1)
            gs.fit(X_train, y_train)
            model.set_params(**gs.best_params_)
            model.fit(X_train, y_train)
            f1 = f1_score(y_test, model.predict(X_test))
            precision = precision_score(y_test, model.predict(X_test))
            recall = recall_score(y_test, model.predict(X_test))
            report[name] = {
                'f1 score': np.round(f1, 2),
                'precision score': np.round(precision, 2),
                'recall score': np.round(recall, 2),
                'Best Params': gs.best_params_
            }
        return report
    except Exception as e:
        raise NetworkSecurityException(e, sys)