from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging
# Configuration for the data ingestion
from network_security.entity.config_entity import DataIngestionConfig
from network_security.entity.artifact_entity import DataIngestionArtifact

import os
import sys
import pandas as pd
import numpy as np
import pymongo
from typing import List
from sklearn.model_selection import train_test_split
from dotenv import load_dotenv
load_dotenv()
MONGO_DB_URI = os.getenv('MONGO_DB_URI')

class DataIngestion:
    def __init__(self, data_ingestion_config:DataIngestionConfig)->None:
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def export_collection_as_dataframe(self)->pd.DataFrame:
        """
        Read Data from MongoDB and return Pandas DataFrame
        """
        try:
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name
            mongo_client = pymongo.MongoClient(MONGO_DB_URI)
            collection = mongo_client[database_name][collection_name]
            df = pd.DataFrame(list(collection.find()))
            if '_id' in df.columns:
                df = df.drop(['_id'], axis=1)
            df = df.replace({'na':np.nan})

            return df
        
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def export_data_into_feature_store(self, dataframe:pd.DataFrame)->pd.DataFrame:
        try:
            feature_store_filepath = self.data_ingestion_config.feature_store_filepath
            #Make Dirs
            dir_path = os.path.dirname(feature_store_filepath)
            os.makedirs(dir_path, exist_ok=True)
            dataframe.to_csv(feature_store_filepath, index=False, header=True)

            return dataframe
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def split_data_as_train_test(self, dataframe:pd.DataFrame)->None:
        try:
            train_set, test_set = train_test_split(
                dataframe,
                test_size=self.data_ingestion_config.train_test_split_ratio
            )
            logging.info('Performed train test split on the dataframe')
            dir_path = os.path.dirname(self.data_ingestion_config.training_filepath)
            os.makedirs(dir_path, exist_ok=True)
            logging.info('Exporting Train and Test data to file')
            train_set.to_csv(self.data_ingestion_config.training_filepath, index=False, header=True)
            test_set.to_csv(self.data_ingestion_config.test_filepath, index=False, header=True)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_data_ingestion(self)->None:
        try:
            dataframe = self.export_collection_as_dataframe()
            dataframe = self.export_data_into_feature_store(dataframe)
            self.split_data_as_train_test(dataframe)
            data_ingestion_artifact = DataIngestionArtifact(
                train_filepath=self.data_ingestion_config.training_filepath,
                test_filepath=self.data_ingestion_config.test_filepath
            )
            return data_ingestion_artifact
        
        except Exception as e:
            raise NetworkSecurityException(e, sys)