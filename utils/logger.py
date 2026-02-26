# utils/logger.py
'''import logging
import os
from datetime import datetime
def configurar_logger():

    if not os.path.exists("logs"):
        os.makedirs("logs")
    
    timestamp = datetime.now().strftime("%d%m%Y-%H%M%S")

    logging.basicConfig(
        filename=f"logs/log_conciliador_bancario_{timestamp}.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        encoding="utf-8"
    )
'''

import logging
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def configurar_logger():

    if not os.path.exists("logs"):
        os.makedirs("logs")

    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    timestamp = datetime.now().strftime("%d%m%Y-%H%M%S")
    logging.basicConfig(
        level=getattr(logging, log_level),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(f"logs/log_conciliador_bancario_{timestamp}.log", encoding="utf-8"),
            logging.StreamHandler()
        ]
    )

