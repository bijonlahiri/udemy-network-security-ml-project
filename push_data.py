import os
import sys
import json
from dotenv import load_dotenv
load_dotenv()

mongodb_uri = os.getenv('MONGO_DB_URI')

import certifi
ca = certifi.where()

import pandas as pd
import numpy as np
import pymongo

from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging

class NetworkDataExtract:
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def csv_to_json_converter(self, filepath):
        try:
            data=pd.read_csv(filepath)
            data = data.reset_index(drop=True)
            records = list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def insert_data_mongodb(self, records, database, collection):
        try:
            mongo_client = pymongo.MongoClient(os.getenv('MONGO_DB_URI'))
            self.database = mongo_client[database]
            self.collection = self.database[collection]
            self.collection.insert_many(records)

            return len(records)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

if __name__=='__main__':
    filepath = 'network_data/phisingData.csv'
    database = 'NetworkDatabase'
    collection = 'Phishing'
    mongodb_inserter = NetworkDataExtract()
    records = mongodb_inserter.csv_to_json_converter(filepath=filepath)
    n_inserted_records = mongodb_inserter.insert_data_mongodb(records=records, database=database, collection=collection)
    print(n_inserted_records)