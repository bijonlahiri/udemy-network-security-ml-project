from network_security.components.data_ingestion import DataIngestion
from network_security.components.data_validation import DataValidation
from network_security.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig, DataValidationConfig
from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging
import sys

if __name__=='__main__':
    try:
        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config)
        logging.info('Initiate the Data Ingestion')
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        print(data_ingestion_artifact)
        logging.info('Data ingestion completed')
        data_validation_config = DataValidationConfig(training_pipeline_config)
        data_validation = DataValidation(data_ingestion_artifact, data_validation_config)
        logging.info('Initiate data validation')
        data_validation_artifact = data_validation.initiate_data_validation()
        print(data_validation_artifact)
        logging.info('Data validation completed')

    except Exception as e:
        raise NetworkSecurityException(e, sys)