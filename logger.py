import logging 
import os
from datetime import datetime

# Prepare logs folder and fils format
LOG_FILE = f"{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.log"
log_path= os.path.join(os.getcwd(), "logs")
os.makedirs(log_path, exist_ok=True)

# create log directory
LOG_FILE_PATH = os.path.join(log_path,LOG_FILE)

# prepare logging config
logging.basicConfig(
    filename=LOG_FILE_PATH,
    level=logging.INFO,
    format='[%(asctime)s] %(lineno)d  %(name)s - %(levelname)s - %(message)s'
)

# instanciate logging obj > logger
logger = logging.getLogger(__name__)

# Check the working of logger odj
logger.info('Logging is set up')


