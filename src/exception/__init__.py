import sys
import logging

def error_message_details(error:Exception, error_details:sys) ->str:
    # Extract trackback details (exception information)
    _,_,exc_tb = error_details.exc_info()
    
    # extrack the trackback details
    file_name = exc_tb.tb_frame.f_code.co_filename
    
    # Create a formatter error message string
    line_number = exc_tb.tb_lineno
    error_message = f"Error occured in script: [{file_name}] at line number: [{line_number}] error message: [{error}]."

    # Log the error for better tracking
    logging.error(error_message)
    
    return error_message

class myException(Exception):

    def __init__(self, error_message:str, error_details:sys):
        super().__init__(error_message)

        self.error_message = error_message_details(error_message, error_details)
    
    def __str__(self):
        return self.error_message