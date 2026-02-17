import sys
from network_security.logging.logger import logging

class NetworkSecurityException(Exception):

    def __init__(self, error_message:str, error_details:sys):
        self.error_message = error_message
        _, _, exc_tb = error_details.exc_info()
        self.lineno = exc_tb.tb_lineno
        self.filename = exc_tb.tb_frame.f_code.co_filename

    def __str__(self)->str:
        return f"\nError:\nFilename: {self.filename}\nLineNo:{self.lineno}\nMessage: {self.error_message}"
