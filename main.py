from network_security.components.data_ingestion import DataIngestion
from network_security.components.data_validation import DataValidation
from network_security.components.data_transformation import DataTransformation
from network_security.entity.config_entity import (
    DataIngestionConfig, TrainingPipelineConfig, DataValidationConfig, DataTransformationConfig
)
from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging
import sys

if __name__=='__main__':
    try:
        ## Pipeline Initialization
        training_pipeline_config = TrainingPipelineConfig()

        ## Data ingestion
        data_ingestion_config = DataIngestionConfig(training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config)
        logging.info('Initiate the Data Ingestion')
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        print(f"\n{data_ingestion_artifact}\n")
        logging.info('Data ingestion completed')

        ## Data validation
        data_validation_config = DataValidationConfig(training_pipeline_config)
        data_validation = DataValidation(data_ingestion_artifact, data_validation_config)
        logging.info('Initiate data validation')
        data_validation_artifact = data_validation.initiate_data_validation()
        print(f"\n{data_validation_artifact}\n")
        logging.info('Data validation completed')

        ## Data transformation
        data_transformation_config = DataTransformationConfig(training_pipeline_config)
        data_transformation = DataTransformation(data_validation_artifact, data_transformation_config)
        logging.info('Initiate data transformation')
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        print(f"\n{data_transformation_artifact}\n")
        logging.info('Data transformation completed')

    except Exception as e:
        raise NetworkSecurityException(e, sys)