import logging

class CustomLogger:
    def __init__(self):
        # Configura el logger
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    def log_info(self, message):
        print(message)
        logging.info(message)

    def log_warning(self, message):
        print(message)
        logging.warning(message)

    def log_error(self, message):
        print(message)
        logging.error(message)