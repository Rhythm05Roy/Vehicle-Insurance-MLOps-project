# Check logger
# from src.logger import logging
# logging.debug("This is a debug message")
# logging.info("This is an info message")
# logging.warning("This is a warning message")
# logging.error("This is an error message")
# logging.critical('This is a critical message')

## Check exception

# from src.logger import logging
# from src.exception import myException
# import sys
# try:
#     a = 1/0
# except Exception as e:
#     logging.info(e)
#     raise myException(e, sys) from e

# mongodb+srv://vikashdas770:WtwsW3eh6T3J0h6z@cluster0.0aygk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0

from src.pipline.training_pipeline import TrainPipeline
pipeline = TrainPipeline()
pipeline.run_pipeline()
