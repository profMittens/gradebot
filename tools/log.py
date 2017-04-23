import logging

def logMsg(config, msg):
    if config.debug:
        print(msg)
    logging.info(msg)
