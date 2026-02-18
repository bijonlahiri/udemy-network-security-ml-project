import os, sys
from typing import List
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
from network_security.constant.training_pipeline import TARGET_COLUMN
from network_security.constant.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS
from network_security.entity.artifact_entity import DataTransformationArtifact, DataValidationArtifact
from network_security.entity.config_entity import DataTransformationConfig
from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging
from network_security.utils.main_utils.utils import save_numpy_array_data, save_object

class DataTransformation:

    def __init__(self,
                 data_validation_artifact: DataValidationArtifact,
                 data_transformation_config: DataTransformationConfig):
        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    @staticmethod
    def read_data(filepath: str) -> pd.DataFrame:
        try:
            return pd.read_csv(filepath)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    @staticmethod
    def drop_target(dataframe: pd.DataFrame, target_column: List[str]) -> pd.DataFrame:
        try:
            df = dataframe
            for column in target_column:
                if column in df.columns:
                    df = df.drop(column, axis=1)
            return df
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    @staticmethod
    def map_target_category(dataframe:pd.DataFrame, target_column: str, map_dict:List[dict])->pd.DataFrame:
        try:
            for i, column in enumerate(target_column):
                df = dataframe[column].map(map_dict[i])
            return df
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def get_data_transformer_object(cls)->Pipeline:
        """
        It initializes a KNN Imputer object with the parameters specified in the training_pipeline __init__.py file
        and returns a Pipeline object with the KNNImputer object as the first step.
        
        :param cls: Description
        :return: Description
        :rtype: Pipeline
        """
        logging.info('Entered the get_data_transformer_object method of the transformer class')
        try:
            imputer:KNNImputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            logging.info(f"Initialize imputer with params: {DATA_TRANSFORMATION_IMPUTER_PARAMS}")
            processor: Pipeline = Pipeline([("imputer", imputer)])
            return processor
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def initiate_data_transformation(self) -> DataTransformationArtifact:
        logging.info('Initiate Data transformation')
        try:
            validation_status = self.data_validation_artifact.validation_status
            if validation_status:
                train_df = DataTransformation.read_data(self.data_validation_artifact.valid_train_filepath)
                test_df = DataTransformation.read_data(self.data_validation_artifact.valid_test_filepath)

                ## Training dataframe
                input_feature_train_df = DataTransformation.drop_target(train_df, TARGET_COLUMN)
                target_feature_train_df = train_df[TARGET_COLUMN]
                target_feature_train_df = DataTransformation.map_target_category(
                    target_feature_train_df,
                    TARGET_COLUMN,
                    [{-1:0, 1:1}]
                )

                ## Test dataframe
                input_feature_test_df = DataTransformation.drop_target(test_df, TARGET_COLUMN)
                target_feature_test_df = test_df[TARGET_COLUMN]
                target_feature_test_df = DataTransformation.map_target_category(
                    target_feature_test_df,
                    TARGET_COLUMN,
                    [{-1:0, 1:1}]
                )

                ## Get Imputer preprocessor
                preprocessor = self.get_data_transformer_object()
                preprocessor_obj = preprocessor.fit(input_feature_train_df)
                transformed_input_feature_train_df = preprocessor_obj.transform(input_feature_train_df)
                transformed_input_feature_test_df = preprocessor_obj.transform(input_feature_test_df)

                ## Combine input and target into a numpy array
                train_array = np.c_[transformed_input_feature_train_df, np.array(target_feature_train_df)]
                test_array = np.c_[transformed_input_feature_test_df, np.array(target_feature_test_df)]

                ## Save numpy array
                save_numpy_array_data(self.data_transformation_config.transformed_train_filepath, train_array)
                save_numpy_array_data(self.data_transformation_config.transformed_test_filepath, test_array)

                ## Save preprocessor object
                save_object(self.data_transformation_config.transformed_object_filepath, preprocessor_obj)

                ## Preparing Artifacts
                data_transformation_artifact = DataTransformationArtifact(
                    transformed_object_filepath=self.data_transformation_config.transformed_object_filepath,
                    transformed_train_filepath=self.data_transformation_config.transformed_train_filepath,
                    transformed_test_filepath=self.data_transformation_config.transformed_test_filepath
                )

                return data_transformation_artifact
            else:
                logging.info('Validation result invalid, skipping transformation')
                ## Preparing Artifacts
                data_transformation_artifact = DataTransformationArtifact(
                    transformed_object_filepath=None,
                    transformed_train_filepath=None,
                    transformed_test_filepath=None 
                )
        
        except Exception as e:
            raise NetworkSecurityException(e, sys)