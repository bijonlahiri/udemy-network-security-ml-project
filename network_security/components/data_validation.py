from network_security.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from network_security.entity.config_entity import DataValidationConfig
from network_security.constant.training_pipeline import SCHEMA_FILEPATH
from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging
from network_security.utils.main_utils.utils import read_yaml_file, write_yaml_file
from scipy.stats import ks_2samp
import pandas as pd
import os, sys

class DataValidation:
    def __init__(self,
                 data_ingestion_artifact:DataIngestionArtifact,
                 data_validation_config:DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILEPATH)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    @staticmethod
    def read_data(filepath: str)->pd.DataFrame:
        try:
            return pd.read_csv(filepath)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def validate_number_of_columns(self, dataframe:pd.DataFrame)->bool:
        try:
            number_of_columns = len(self._schema_config['columns'])
            logging.info(f"Required No. of columns: {number_of_columns}")
            logging.info(f"Dataframe has columns: {len(dataframe.columns)}")
            if len(dataframe.columns)==number_of_columns:
                return True
            return False
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def detect_dataset_drift(self, base_df:pd.DataFrame, current_df:pd.DataFrame, threshold=0.05)->bool:
        try:
            status=True
            report={}
            for column in base_df.columns:
                d1=base_df[column]
                d2=current_df[column]
                is_same_dist=ks_2samp(d1, d2)
                if threshold<=is_same_dist.pvalue:
                    is_found=False
                else:
                    is_found=True
                    status=False
                report.update({column:{
                    'p_value': float(is_same_dist.pvalue),
                    'drift_status': is_found
                }})
            ## Create report directory
            drift_report_filepath = self.data_validation_config.drift_report_filepath
            dir_path = os.path.dirname(drift_report_filepath)
            os.makedirs(dir_path, exist_ok=True)
            write_yaml_file(filepath=drift_report_filepath, content=report)
            return status
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_data_validation(self)->DataValidationArtifact:
        try:
            train_filepath = self.data_ingestion_artifact.train_filepath
            test_filepath = self.data_ingestion_artifact.test_filepath

            # Read the dataframe for train and test
            train_dataframe = DataValidation.read_data(train_filepath)
            test_dataframe = DataValidation.read_data(test_filepath)

            ## Validate columns for train and test data
            status = self.validate_number_of_columns(dataframe=train_dataframe)
            if not status:
                error_message = f"Train dataframe does not contain all columns.\n"
                logging.info(f'{error_message}')
            status = self.validate_number_of_columns(dataframe=test_dataframe)
            if not status:
                error_message = f"Test dataframe does not contain all the columns.\n"
                logging.info(f'{error_message}')

            ## Check data drift
            status = self.detect_dataset_drift(base_df=train_dataframe, current_df=test_dataframe)
            logging.info(f'Drift Status: {status}')
            if status:
                dir_path = os.path.dirname(self.data_validation_config.valid_train_data_filepath)
                os.makedirs(dir_path, exist_ok=True)
                train_dataframe.to_csv(self.data_validation_config.valid_train_data_filepath, index=False, header=True)
                test_dataframe.to_csv(self.data_validation_config.valid_test_data_filepath, index=False, header=True)
                data_validation_artifact = DataValidationArtifact(
                    validation_status=status,
                    valid_train_filepath=self.data_validation_config.valid_train_data_filepath,
                    valid_test_filepath=self.data_validation_config.valid_test_data_filepath,
                    invalid_train_filepath=None,
                    invalid_test_filepath=None,
                    drift_report_filepath=self.data_validation_config.drift_report_filepath
                )
            else:
                dir_path = os.path.dirname(self.data_validation_config.invalid_train_data_filepath)
                os.makedirs(dir_path, exist_ok=True)
                train_dataframe.to_csv(self.data_validation_config.invalid_train_data_filepath, index=False, header=True)
                test_dataframe.to_csv(self.data_validation_config.invalid_test_data_filepath)
                data_validation_artifact = DataValidationArtifact(
                    validation_status=status,
                    valid_train_filepath=None,
                    valid_test_filepath=None,
                    invalid_train_filepath=self.data_validation_config.invalid_train_data_filepath,
                    invalid_test_filepath=self.data_validation_config.invalid_test_data_filepath,
                    drift_report_filepath=self.data_validation_config.drift_report_filepath
                )
            return data_validation_artifact
            
        except Exception as e:
            raise NetworkSecurityException(e, sys)