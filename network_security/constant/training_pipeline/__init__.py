import os
import sys
import pandas as pd
import numpy as np

"""
Define common constant variables for training pipeline
"""

TARGET_COLUMN = ['Result']
PIPELINE_NAME = 'NetworkSecurity'
ARTIFACT_DIR = 'Artifacts'
FILENAME = 'phishingData.csv'
TRAIN_FILENAME = 'train.csv'
TEST_FILENAME = 'test.csv'

SCHEMA_FILEPATH = os.path.join('data_schema', 'schema.yaml')

"""
Data Ingestion related constants start with DATA_INGESTION VAR NAME
"""

DATA_INGESTION_COLLECTION_NAME: str = 'Phishing'
DATA_INGESTION_DATABASE_NAME: str = 'NetworkDatabase'
DATA_INGESTION_DIR_NAME: str = 'data_ingestion'
DATA_INGESTION_FEATURE_STORE_DIR: str = 'feature_store'
DATA_INGESTION_INGESTED_DIR: str = 'ingested'
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2

"""
Data Validation related constants starts with DATA_VALIDATION VAR NAME
"""

DATA_VALIDATION_DIR_NAME: str = 'data_validation'
DATA_VALIDATION_VALID_DIR: str = 'validated'
DATA_VALIDATION_INVALID_DIR: str = 'invalid'
DATA_VALIDATION_DRIFT_REPORT_DIR: str = 'drift_report'
DATA_VALIDATION_DRIFT_REPORT_FILENAME: str = 'report.yaml'

"""
Data transformation related constants starts with DATA_TRANSFORMATION VAR NAME
"""

PREPROCESSING_OBJECT_FILENAME: str = 'preprocessing.pkl'

DATA_TRANSFORMATION_DIR_NAME: str = 'data_transformation'
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR: str = 'transformed'
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR: str = 'transformed_object'

"""
KNN Imputer Params to replace NAN values
"""
DATA_TRANSFORMATION_IMPUTER_PARAMS: dict = {
    'missing_values': np.nan,
    'n_neighbors': 3,
    'weights': 'uniform'
}