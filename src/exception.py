import sys
from src.logger import logger

def error_message_details(error, error_detail: sys):
    """generate a detailed error messages including file name and line information """
    _, _, exc_tb = error_detail.exc_info()
    filename = exc_tb.tb_frame.f_code.co_filename
    line_number = exc_tb.tb_lineno
    return f"Error occurred in file: {filename} at line number: {line_number} with message: {str(error)}"

class CustomException(Exception):
    def __init__(self, exception, error_detail: sys):
        super().__init__(exception)
        self.error_message = error_message_details(exception, error_detail=error_detail)
        
    def __str__(self):
        return self.error_message
    
    
if __name__ == "__main__":
    try: 
        d = 1/1
    except Exception as e:
        raise CustomException(e, sys)