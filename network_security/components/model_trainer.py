import os, sys
import numpy as np
from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging
from network_security.entity.config_entity import ModelTrainerConfig
from network_security.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact
from network_security.utils.main_utils.utils import save_object, load_object, load_numpy_array_data
from network_security.utils.ml_utils.metric.classification_metric import get_metric_artifact
from network_security.utils.ml_utils.model.estimator import NetworkModel
from network_security.utils.ml_utils.model.model_evaluation import evaluate_models

from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    AdaBoostClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier
)

class ModelTrainer:

    def __init__(self, data_transformation_artifact: DataTransformationArtifact, model_trainer_config: ModelTrainerConfig):
        try:
            self.data_transformation_artifact = data_transformation_artifact
            self.model_trainer_config = model_trainer_config
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def train_model(self, X_train:np.array, y_train:np.array, X_test:np.array, y_test:np.array)->ModelTrainerArtifact:
        try:
            models = {
                'Random Forest': RandomForestClassifier(verbose=1),
                'Decision Tree': DecisionTreeClassifier(),
                'Gradient Boosting': GradientBoostingClassifier(verbose=1),
                'Logistic Regression': LogisticRegression(verbose=1),
                'Adaboost Classifier': AdaBoostClassifier()
            }
            params = {
                'Decision Tree': {
                    'criterion': ['gini', 'entropy', 'log_loss']
                },
                'Random Forest': {
                    'n_estimators': [8, 16, 32, 64, 128, 256]
                },
                'Gradient Boosting': {
                    'learning_rate': [0.1, 0.01, 0.05, 0.001],
                    'subsample': [0.6, 0.7, 0.75, 0.8, 0.85, 0.9],
                    'n_estimators': [8, 16, 32, 64, 128, 256]
                },
                'Logistic Regression': {},
                'Adaboost Classifier': {
                    'learning_rate': [0.1, 0.01, 0.05, 0.001],
                    'n_estimators': [8, 16, 32, 64, 128, 256]
                }
            }
            model_report: dict = evaluate_models(
                X_train=X_train,
                X_test=X_test,
                y_train=y_train,
                y_test=y_test,
                models=models,
                params=params
            )
            best_model_f1_score = max([report['f1 score'] for report in model_report.values()])
            best_model_name = [name for name, report in model_report.items() if report['f1 score']==best_model_f1_score][0]
            best_model = models[best_model_name]
            best_model.set_params(**model_report[best_model_name]['Best Params'])
            logging.info(f"Best Model: {best_model_name}\nBest Params:\n{model_report[best_model_name]['Best Params']}\n")
            y_train_pred = best_model.predict(X_train)
            classification_train_metric = get_metric_artifact(y_true=y_train, y_pred=y_train_pred)

            ## Track the MLFLOW
            y_test_pred = best_model.predict(X_test)
            classification_test_metric = get_metric_artifact(y_true=y_test, y_pred=y_test_pred)

            preprocessor = load_object(self.data_transformation_artifact.transformed_object_filepath)
            model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_filepath)
            os.makedirs(model_dir_path, exist_ok=True)
            network_model = NetworkModel(preprocessor=preprocessor, model=best_model)
            save_object(self.model_trainer_config.trained_model_filepath, obj=network_model)

            ## Model Trainer Artifact
            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_filepath=self.model_trainer_config.trained_model_filepath,
                train_metric_artifact=classification_train_metric,
                test_metric_artifact=classification_test_metric
            )
            logging.info(f'Model trainer artifact: {model_trainer_artifact}')

            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            train_filepath = self.data_transformation_artifact.transformed_train_filepath
            test_filepath = self.data_transformation_artifact.transformed_test_filepath
            if train_filepath:
                train_array = load_numpy_array_data(train_filepath)
                test_array = load_numpy_array_data(test_filepath)

                X_train, y_train, X_test, y_test = (
                    train_array[:, :-1],
                    train_array[:, -1],
                    test_array[:, :-1],
                    test_array[:, -1]
                )
                return self.train_model(
                    X_train=X_train,
                    X_test=X_test,
                    y_train=y_train,
                    y_test=y_test
                )
            else:
                logging.info('Invalid data, skipping model training')
                model_trainer_artifact = ModelTrainerArtifact(
                    trained_model_filepath=None,
                    train_metric_artifact=None,
                    test_metric_artifact=None
                )
                return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)