import yaml
from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging
import os, sys
import numpy as np
import dill
import pickle

def read_yaml_file(filepath: str)->dict:
    try:
        with open(filepath, 'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise NetworkSecurityException(e, sys)

def write_yaml_file(filepath: str, content: object, replace: bool=True)->None:
    try:
        if replace:
            if os.path.exists(filepath):
                os.remove(filepath)
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as yaml_file:
            yaml.dump(content, yaml_file)
    except Exception as e:
        raise NetworkSecurityException(e, sys)

def save_numpy_array_data(filepath: str, array: np.array) -> None:
    """
    Save Numpy array data to file
    """
    try:
        dir_path = os.path.dirname(filepath)
        os.makedirs(dir_path, exist_ok=True)
        with open(filepath, 'wb') as file:
            np.save(file, array)
        logging.info('Saved Numpy array')
    except Exception as e:
        raise NetworkSecurityException(e, sys)

def save_object(filepath: str, obj: object) -> None:
    try:
        dir_path = os.path.dirname(filepath)
        os.makedirs(dir_path, exist_ok=True)
        with open(filepath, 'wb') as file:
            pickle.dump(obj, file)
        logging.info('Saved object to file')
    except Exception as e:
        raise NetworkSecurityException(e, sys)

def load_object(filepath: str)->object:
    try:
        if not os.path.exists(filepath):
            raise Exception(f'Object filepath {filepath} does not exist.')
        with open(filepath, 'rb') as object_file:
            return pickle.load(object_file)
    except Exception as e:
        raise NetworkSecurityException(e, sys)

def load_numpy_array_data(filepath: str)->np.array:
    """
    Load numpy array data from file
    """
    try:
        if not os.path.exists(filepath):
            raise Exception(f'Numpy array file {filepath} does not exist.')
        with open(filepath, 'rb') as numpy_file:
            return np.load(numpy_file)
    except Exception as e:
        raise NetworkSecurityException(e, sys)