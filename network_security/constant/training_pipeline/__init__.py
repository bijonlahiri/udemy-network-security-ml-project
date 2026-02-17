import os
import sys
import pandas as pd
import numpy as np

"""
Define common constant variables for training pipeline
"""

TARGET_COLUMN = 'Result'
PIPELINE_NAME = 'NetworkSecurity'
ARTIFACT_DIR = 'Artifacts'
FILENAME = 'phishingData.csv'
TRAIN_FILENAME = 'train.csv'
TEST_FILENAME = 'test.csv'

"""
Data Ingestion related constants start with DATA_INGESTION VAR NAME
"""

DATA_INGESTION_COLLECTION_NAME: str = 'Phishing'
DATA_INGESTION_DATABASE_NAME: str = 'NetworkDatabase'
DATA_INGESTION_DIR_NAME: str = 'data_ingestion'
DATA_INGESTION_FEATURE_STORE_DIR: str = 'feature_store'
DATA_INGESTION_INGESTED_DIR: str = 'ingested'
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2