import os
import logging
from datetime import datetime

class CustomLogger:

    def __init__(self, log_dir='logs'):

        self.log_dir = os.path.join(os.getcwd(), log_dir)
        os.makedirs(self.log_dir, exist_ok=True)
        log_file = f"{datetime.now().strftime('%m_%d_%y_%H_%M_%S')}.log"
        self.log_file_path = os.path.join(self.log_dir, log_file)
        logging.basicConfig(
            filename=self.log_file_path,
            format= '[%(asctime)s] %(levelname)s %(name)s (line: %(lineno)d) - %(message)s',
            level=logging.INFO
        )

    def get_logger(self, name = __file__):
        return logging.getLogger(os.path.basename(name))