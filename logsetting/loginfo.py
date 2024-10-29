import logging

logging.basicConfig(filename='openhis.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

def log_info(message):
    logging.info(message)